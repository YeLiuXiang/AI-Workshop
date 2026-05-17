from __future__ import annotations

import json
import mimetypes
import re
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from workshop_service.config import Settings, load_settings
from workshop_service.job_store import JobStore
from workshop_service.models import ArtifactRecord, JobMode, JobStage, JobStatus, WorkshopJobRequest
from workshop_service.pipeline import WorkshopPipeline, write_request_json


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip())
    return cleaned or "upload.bin"


def enrich_request(request: WorkshopJobRequest) -> WorkshopJobRequest:
    payload = request.model_dump(mode="json")
    workshop = payload.setdefault("workshop", {})
    event_input = payload.setdefault("event_input", {})
    mvp_spec = payload.setdefault("mvp_spec", {})

    scene_name = str(event_input.get("scene_name") or workshop.get("customer") or "").strip()
    industry = str(workshop.get("industry") or event_input.get("customer_type") or "").strip()

    if scene_name and not workshop.get("customer"):
        workshop["customer"] = scene_name
    if scene_name and not event_input.get("prototype_preference"):
        workshop_name = scene_name if scene_name.endswith("工作台") else f"{scene_name}工作台"
        event_input["prototype_preference"] = workshop_name
    if industry and not event_input.get("customer_type"):
        event_input["customer_type"] = industry

    workshop.setdefault("title", "AI Discovery Card Workshop")
    workshop.setdefault("group_name", "现场共创组")
    workshop.setdefault("date", datetime.now().strftime("%Y-%m-%d"))
    mvp_spec.setdefault("tech_stack_preference", "Next.js + Tailwind CSS")

    return WorkshopJobRequest.model_validate(payload)


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or load_settings()
    store = JobStore(app_settings.job_root)
    pipeline = WorkshopPipeline(app_settings)
    app = FastAPI(title="Workshop Generation Service", version="0.1.0")
    web_dir = app_settings.project_root / "workshop_service" / "web"
    app.mount("/static", StaticFiles(directory=web_dir), name="static")

    def run_job(job_id: str, request: WorkshopJobRequest) -> None:
        job_dir = store.job_dir(job_id)
        store.update_job(
            job_id,
            status=JobStatus.running,
            stage=JobStage.queued,
            stage_label="任务已启动",
        )
        try:
            def update_stage(stage: str, label: str) -> None:
                store.update_job(job_id, stage=stage, stage_label=label)

            result = pipeline.execute(
                store.get_job(job_id),
                request,
                job_dir,
                progress_callback=update_stage,
            )
            store.update_job(
                job_id,
                status=JobStatus.succeeded,
                stage=JobStage.completed,
                stage_label="已完成，结果可下载",
                case_dir=str(result.case_dir),
                scenario_path=str(result.scenario_path) if result.scenario_path else None,
                artifacts=result.artifacts,
                prototype_status="succeeded" if request.options.generate_prototype else "not_requested",
                prototype_label="原型已完成" if request.options.generate_prototype else "可单独生成原型",
                prototype_error=None,
                logs=result.logs,
            )
        except Exception as exc:
            failure_logs = {}
            logs_dir = job_dir / "logs"
            if logs_dir.exists():
                for path in logs_dir.glob("*.log"):
                    failure_logs[path.stem] = str(path)
            store.update_job(
                job_id,
                status=JobStatus.failed,
                stage=JobStage.failed,
                stage_label="任务失败",
                error=str(exc),
                logs=failure_logs,
            )

    def run_prototype(job_id: str) -> None:
        job = store.get_job(job_id)
        if not job.case_dir:
            store.update_job(
                job_id,
                prototype_status="failed",
                prototype_label="原型生成失败",
                prototype_error="缺少方案输出目录，无法生成原型",
            )
            return
        store.update_job(
            job_id,
            prototype_status="running",
            prototype_label="正在生成演示原型",
            prototype_error=None,
        )
        try:
            artifacts = pipeline.generate_prototype(
                Path(job.case_dir),
                Path(job.scenario_path) if job.scenario_path else None,
            )
            store.update_job(
                job_id,
                artifacts=artifacts,
                prototype_status="succeeded",
                prototype_label="原型已完成",
                prototype_error=None,
            )
        except Exception as exc:
            store.update_job(
                job_id,
                prototype_status="failed",
                prototype_label="原型生成失败",
                prototype_error=str(exc),
            )

    @app.get("/")
    def root():
        return FileResponse(web_dir / "index.html")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {
            "status": "ok",
            "project_root": str(app_settings.project_root),
            "output_root": str(app_settings.output_root),
            "default_mode": app_settings.codex_default_mode,
        }

    @app.get("/api/meta")
    def meta() -> dict[str, object]:
        return {
            "default_mode": app_settings.codex_default_mode,
            "supported_modes": [mode.value for mode in JobMode],
        }

    @app.post("/api/jobs/json")
    def create_json_job(
        request: WorkshopJobRequest,
        background_tasks: BackgroundTasks,
    ) -> dict[str, str]:
        request = enrich_request(request)
        mode = request.options.mode or JobMode(app_settings.codex_default_mode)
        temp_job_id = "new"
        request_path = app_settings.job_root / temp_job_id / "request.json"
        record = store.create_job(mode, request_path)
        request_path = store.job_dir(record.job_id) / "request.json"
        write_request_json(request, request_path)
        store.update_job(record.job_id, request_path=str(request_path))
        background_tasks.add_task(run_job, record.job_id, request)
        return {"job_id": record.job_id, "status": JobStatus.queued.value}

    @app.post("/api/jobs/form")
    async def create_form_job(
        background_tasks: BackgroundTasks,
        payload_json: str = Form(...),
        files: list[UploadFile] = File(default_factory=list),
    ) -> dict[str, str]:
        try:
            payload = json.loads(payload_json)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail=f"Invalid payload_json: {exc}") from exc

        request = enrich_request(WorkshopJobRequest.model_validate(payload))
        mode = request.options.mode or JobMode(app_settings.codex_default_mode)
        temp_job_id = "new"
        request_path = app_settings.job_root / temp_job_id / "request.json"
        record = store.create_job(mode, request_path)
        job_dir = store.job_dir(record.job_id)
        uploads_dir = job_dir / "uploads"
        uploads_dir.mkdir(parents=True, exist_ok=True)

        uploaded_paths: list[str] = []
        for upload in files:
            target = uploads_dir / sanitize_filename(upload.filename or "upload.bin")
            content = await upload.read()
            target.write_bytes(content)
            uploaded_paths.append(str(target))

        merged_payload = request.model_dump(mode="json")
        merged_payload["card_photo_paths"] = list(request.card_photo_paths) + uploaded_paths
        merged_request = WorkshopJobRequest.model_validate(merged_payload)

        request_path = job_dir / "request.json"
        write_request_json(merged_request, request_path)
        store.update_job(record.job_id, request_path=str(request_path))
        background_tasks.add_task(run_job, record.job_id, merged_request)
        return {"job_id": record.job_id, "status": JobStatus.queued.value}

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str):
        try:
            return store.get_job(job_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Job not found") from exc

    @app.post("/api/jobs/{job_id}/prototype")
    def create_prototype_job(job_id: str, background_tasks: BackgroundTasks) -> dict[str, str]:
        try:
            job = store.get_job(job_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Job not found") from exc
        if job.status != JobStatus.succeeded:
            raise HTTPException(status_code=409, detail="PPT 方案尚未完成")
        if job.prototype_status == "running":
            raise HTTPException(status_code=409, detail="原型正在生成中")
        store.update_job(
            job_id,
            prototype_status="queued",
            prototype_label="原型任务已提交",
            prototype_error=None,
        )
        background_tasks.add_task(run_prototype, job_id)
        return {"job_id": job_id, "prototype_status": "queued"}

    @app.get("/api/jobs/{job_id}/artifacts")
    def get_job_artifacts(job_id: str) -> list[ArtifactRecord]:
        try:
            return store.list_artifacts(job_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Job not found") from exc

    @app.get("/api/jobs/{job_id}/artifacts/{artifact_name:path}")
    def download_artifact(job_id: str, artifact_name: str, download: bool = False):
        try:
            job = store.get_job(job_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Job not found") from exc
        if job.status != JobStatus.succeeded:
            raise HTTPException(status_code=409, detail="Artifacts are not ready")
        case_dir = Path(job.case_dir or "")
        target = (case_dir / artifact_name).resolve()
        if not case_dir.exists() or not target.exists() or case_dir.resolve() not in target.parents and case_dir.resolve() != target.parent:
            raise HTTPException(status_code=404, detail="Artifact not found")
        media_type = mimetypes.guess_type(str(target))[0]
        if download:
            return FileResponse(path=target, filename=target.name, media_type=media_type)
        return FileResponse(path=target, media_type=media_type)

    return app


def main() -> None:
    settings = load_settings()
    uvicorn.run(
        create_app(settings),
        host=settings.service_host,
        port=settings.service_port,
    )
