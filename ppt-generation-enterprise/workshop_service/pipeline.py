from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from workshop_service.codex_cli import CodexCliRunner
from workshop_service.config import Settings
from workshop_service.models import ArtifactRecord, JobMode, JobRecord, JobStatus, WorkshopJobRequest
from workshop_service.prompting import build_codex_prompt


@dataclass
class PipelineRunResult:
    case_dir: Path
    artifacts: list[ArtifactRecord]
    logs: dict[str, str]
    scenario_path: Path | None = None


class WorkshopPipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.codex_runner = CodexCliRunner(settings)

    def execute(
        self,
        job: JobRecord,
        request: WorkshopJobRequest,
        job_dir: Path,
    ) -> PipelineRunResult:
        request_path = Path(job.request_path)
        mode = request.options.mode or JobMode(self.settings.codex_default_mode)
        logs: dict[str, str] = {}
        scenario_path: Path | None = None
        before_dirs = {
            str(path.resolve())
            for path in self.settings.output_root.iterdir()
            if self.settings.output_root.exists() and path.is_dir()
        } if self.settings.output_root.exists() else set()

        if mode == JobMode.codex_cli:
            scenario_path = job_dir / "normalized-scenario.json"
            image_paths = self._resolve_image_paths(request, request_path, job_dir)
            prompt = build_codex_prompt(
                self.settings.codex_prompt_template,
                self._display_path(request_path),
                self._display_path(scenario_path),
                [self._display_path(path) for path in image_paths],
            )
            codex_result = self.codex_runner.run(
                prompt=prompt,
                workdir=self.settings.project_root,
                image_paths=image_paths,
                timeout_seconds=request.options.timeout_seconds,
            )
            logs["codex_stdout"] = codex_result.stdout
            logs["codex_stderr"] = codex_result.stderr
            logs["codex_command"] = " ".join(codex_result.command)
            if codex_result.returncode != 0:
                raise RuntimeError(
                    f"Codex CLI failed with exit code {codex_result.returncode}"
                )
            normalized_output = codex_result.stdout.strip()
            if not normalized_output:
                raise RuntimeError("Codex CLI finished without returning normalized scenario JSON")
            json.loads(normalized_output)
            scenario_path.write_text(normalized_output + "\n", encoding="utf-8")
            input_path = scenario_path
            fast_mode = False
        else:
            input_path = request_path
            fast_mode = mode == JobMode.python_fast

        generator_result = self._run_generator(
            input_path=input_path,
            fast_mode=fast_mode,
            options=request.options.model_dump(),
            timeout_seconds=request.options.timeout_seconds,
        )
        logs["generator_stdout"] = generator_result.stdout
        logs["generator_stderr"] = generator_result.stderr
        logs["generator_command"] = " ".join(generator_result.args)
        if generator_result.returncode != 0:
            raise RuntimeError(
                f"Workshop generator failed with exit code {generator_result.returncode}"
            )

        case_dir = self._extract_case_dir(generator_result.stdout, before_dirs)
        artifacts = self._collect_artifacts(case_dir)
        return PipelineRunResult(
            case_dir=case_dir,
            artifacts=artifacts,
            logs=logs,
            scenario_path=scenario_path,
        )

    def _run_generator(
        self,
        input_path: Path,
        fast_mode: bool,
        options: dict[str, Any],
        timeout_seconds: int,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            self.settings.python_bin,
            "scripts/generate_workshop_package.py",
            "--input",
            str(input_path),
            "--workspace-root",
            str(self.settings.output_root),
            "--template",
            str(options.get("template") or "enterprise-forum"),
            "--theme",
            str(options.get("theme") or "eden-enterprise"),
            "--aspect-ratio",
            str(options.get("aspect_ratio") or "16:9"),
        ]
        if fast_mode:
            command.append("--fast")

        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            cwd=self.settings.project_root,
            env={
                **os.environ,
                "PYTHONIOENCODING": "utf-8",
            },
            shell=False,
        )

    def _resolve_image_paths(
        self,
        request: WorkshopJobRequest,
        request_path: Path,
        job_dir: Path,
    ) -> list[Path]:
        input_dir = request_path.parent
        resolved: list[Path] = []
        for raw_path in request.card_photo_paths:
            candidate = Path(raw_path)
            if not candidate.is_absolute():
                candidate = (input_dir / raw_path).resolve()
            if candidate.exists():
                resolved.append(candidate)
        uploads_dir = job_dir / "uploads"
        if uploads_dir.exists():
            resolved.extend(path for path in uploads_dir.iterdir() if path.is_file())
        deduped: list[Path] = []
        seen = set()
        for path in resolved:
            marker = str(path.resolve())
            if marker not in seen:
                deduped.append(path.resolve())
                seen.add(marker)
        return deduped

    def _display_path(self, path: Path) -> Path:
        try:
            return path.resolve().relative_to(self.settings.project_root)
        except ValueError:
            return path.resolve()

    def _extract_case_dir(self, stdout: str, before_dirs: set[str]) -> Path:
        for line in reversed([line.strip() for line in stdout.splitlines() if line.strip()]):
            candidate = Path(line)
            if not candidate.is_absolute():
                candidate = (self.settings.project_root / candidate).resolve()
            if candidate.exists() and candidate.is_dir():
                return candidate
        if self.settings.output_root.exists():
            after_dirs = [
                path.resolve()
                for path in self.settings.output_root.iterdir()
                if path.is_dir()
            ]
            new_dirs = [path for path in after_dirs if str(path) not in before_dirs]
            if len(new_dirs) == 1:
                return new_dirs[0]
        raise RuntimeError("Unable to determine output case directory from generator stdout")

    def _collect_artifacts(self, case_dir: Path) -> list[ArtifactRecord]:
        allowed_suffixes = {".pptx", ".md", ".json", ".html", ".css", ".js", ".png"}
        artifacts: list[ArtifactRecord] = []
        for path in sorted(case_dir.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in allowed_suffixes:
                continue
            artifacts.append(
                ArtifactRecord(
                    name=path.relative_to(case_dir).as_posix(),
                    path=str(path),
                    size_bytes=path.stat().st_size,
                )
            )
        return artifacts


def write_request_json(request: WorkshopJobRequest, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            request.model_dump(mode="json", exclude_none=True),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
