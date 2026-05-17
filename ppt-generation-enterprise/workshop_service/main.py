from __future__ import annotations

import json
import re
from pathlib import Path

import uvicorn
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from workshop_service.config import Settings, load_settings
from workshop_service.job_store import JobStore
from workshop_service.models import ArtifactRecord, JobMode, JobStatus, WorkshopJobRequest
from workshop_service.pipeline import WorkshopPipeline, write_request_json


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip())
    return cleaned or "upload.bin"


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or load_settings()
    store = JobStore(app_settings.job_root)
    pipeline = WorkshopPipeline(app_settings)
    app = FastAPI(title="Workshop Generation Service", version="0.1.0")

    def run_job(job_id: str, request: WorkshopJobRequest) -> None:
        job_dir = store.job_dir(job_id)
        store.update_job(job_id, status=JobStatus.running)
        try:
            result = pipeline.execute(store.get_job(job_id), request, job_dir)
            store.update_job(
                job_id,
                status=JobStatus.succeeded,
                case_dir=str(result.case_dir),
                scenario_path=str(result.scenario_path) if result.scenario_path else None,
                artifacts=result.artifacts,
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
                error=str(exc),
                logs=failure_logs,
            )

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {
            "status": "ok",
            "project_root": str(app_settings.project_root),
            "output_root": str(app_settings.output_root),
            "default_mode": app_settings.codex_default_mode,
        }

    @app.post("/api/jobs/json")
    def create_json_job(
        request: WorkshopJobRequest,
        background_tasks: BackgroundTasks,
    ) -> dict[str, str]:
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

        request = WorkshopJobRequest.model_validate(payload)
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

    @app.get("/api/jobs/{job_id}/artifacts")
    def get_job_artifacts(job_id: str) -> list[ArtifactRecord]:
        try:
            return store.list_artifacts(job_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Job not found") from exc

    @app.get("/api/jobs/{job_id}/artifacts/{artifact_name:path}")
    def download_artifact(job_id: str, artifact_name: str):
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
        return FileResponse(path=target, filename=target.name)

    return app


def main() -> None:
    settings = load_settings()
    uvicorn.run(
        create_app(settings),
        host=settings.service_host,
        port=settings.service_port,
    )
