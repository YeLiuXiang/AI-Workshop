from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class JobMode(str, Enum):
    python_fast = "python-fast"
    python_assets = "python-assets"
    codex_cli = "codex-cli"


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"


class JobStage(str, Enum):
    queued = "queued"
    codex_normalization = "codex-normalization"
    artifact_generation = "artifact-generation"
    prototype_generation = "prototype-generation"
    completed = "completed"
    failed = "failed"


class JobOptions(BaseModel):
    mode: JobMode | None = None
    template: str = "enterprise-forum"
    theme: str = "eden-enterprise"
    aspect_ratio: str = "16:9"
    generate_prototype: bool = False
    timeout_seconds: int = Field(default=900, ge=60, le=3600)


class WorkshopJobRequest(BaseModel):
    workshop: dict[str, Any] = Field(default_factory=dict)
    event_input: dict[str, Any] = Field(default_factory=dict)
    mvp_spec: dict[str, Any] = Field(default_factory=dict)
    current_process: list[str] = Field(default_factory=list)
    detected_cards: dict[str, list[str]] = Field(default_factory=dict)
    recognized_cards: list[Any] = Field(default_factory=list)
    card_photo_paths: list[str] = Field(default_factory=list)
    product_mapping: list[dict[str, Any]] = Field(default_factory=list)
    options: JobOptions = Field(default_factory=JobOptions)


class ArtifactRecord(BaseModel):
    name: str
    path: str
    size_bytes: int


class JobRecord(BaseModel):
    job_id: str
    status: JobStatus
    mode: JobMode
    stage: JobStage = JobStage.queued
    stage_label: str = "等待执行"
    created_at: str
    updated_at: str
    request_path: str
    scenario_path: str | None = None
    case_dir: str | None = None
    artifacts: list[ArtifactRecord] = Field(default_factory=list)
    prototype_status: str = "not_requested"
    prototype_label: str = "尚未生成"
    prototype_error: str | None = None
    error: str | None = None
    logs: dict[str, str] = Field(default_factory=dict)
