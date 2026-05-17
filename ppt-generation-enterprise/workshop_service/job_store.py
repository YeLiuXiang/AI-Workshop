from __future__ import annotations

import json
import threading
import uuid
from pathlib import Path

from workshop_service.models import ArtifactRecord, JobMode, JobRecord, JobStatus, utc_now_iso


class JobStore:
    def __init__(self, job_root: Path) -> None:
        self.job_root = job_root
        self.job_root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def create_job(self, mode: JobMode, request_path: Path) -> JobRecord:
        with self._lock:
            job_id = uuid.uuid4().hex
            job_dir = self.job_root / job_id
            job_dir.mkdir(parents=True, exist_ok=True)
            record = JobRecord(
                job_id=job_id,
                status=JobStatus.queued,
                mode=mode,
                stage_label="等待执行",
                created_at=utc_now_iso(),
                updated_at=utc_now_iso(),
                request_path=str(request_path),
            )
            self._write_record(record)
            return record

    def update_job(self, job_id: str, **changes) -> JobRecord:
        with self._lock:
            record = self.get_job(job_id)
            payload = record.model_dump()
            payload.update(changes)
            payload["updated_at"] = utc_now_iso()
            updated = JobRecord.model_validate(payload)
            self._write_record(updated)
            return updated

    def get_job(self, job_id: str) -> JobRecord:
        path = self._record_path(job_id)
        return JobRecord.model_validate(
            json.loads(path.read_text(encoding="utf-8"))
        )

    def list_artifacts(self, job_id: str) -> list[ArtifactRecord]:
        return self.get_job(job_id).artifacts

    def job_dir(self, job_id: str) -> Path:
        return self.job_root / job_id

    def _record_path(self, job_id: str) -> Path:
        return self.job_dir(job_id) / "status.json"

    def _write_record(self, record: JobRecord) -> None:
        path = self._record_path(record.job_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(record.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
