from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    project_root: Path
    output_root: Path
    job_root: Path
    python_bin: str
    codex_cli_bin: str
    codex_model: str
    codex_reasoning_effort: str
    codex_sandbox: str
    codex_approval_policy: str
    codex_use_ephemeral: bool
    codex_ignore_user_config: bool
    codex_default_mode: str
    codex_prompt_template: Path
    service_host: str
    service_port: int


def load_settings() -> Settings:
    default_project_root = Path(__file__).resolve().parents[1]
    env_file = Path(
        os.getenv("WORKSHOP_ENV_FILE", default_project_root / ".env")
    ).resolve()
    _load_dotenv_file(env_file)
    project_root = Path(
        os.getenv("WORKSHOP_PROJECT_ROOT", default_project_root)
    ).resolve()
    default_output_root = (
        project_root / "workspace"
        if (project_root / "workspace").exists()
        else project_root / "Workspace"
    )
    output_root = Path(
        os.getenv("WORKSHOP_OUTPUT_ROOT", default_output_root)
    ).resolve()
    job_root = Path(
        os.getenv("WORKSHOP_JOB_ROOT", project_root / "runtime" / "jobs")
    ).resolve()
    prompt_template = Path(
        os.getenv(
            "WORKSHOP_CODEX_PROMPT_TEMPLATE",
            project_root / "workshop_service" / "prompts" / "codex_normalize_workshop_prompt.md",
        )
    ).resolve()

    return Settings(
        project_root=project_root,
        output_root=output_root,
        job_root=job_root,
        python_bin=os.getenv("WORKSHOP_PYTHON_BIN", "python"),
        codex_cli_bin=os.getenv("CODEX_CLI_BIN", "codex"),
        codex_model=os.getenv("CODEX_MODEL", "").strip(),
        codex_reasoning_effort=os.getenv("CODEX_REASONING_EFFORT", "low").strip() or "low",
        codex_sandbox=os.getenv("CODEX_SANDBOX", "workspace-write").strip() or "workspace-write",
        codex_approval_policy=os.getenv("CODEX_APPROVAL_POLICY", "never").strip() or "never",
        codex_use_ephemeral=_env_flag("CODEX_USE_EPHEMERAL", True),
        codex_ignore_user_config=_env_flag("CODEX_IGNORE_USER_CONFIG", False),
        codex_default_mode=os.getenv("WORKSHOP_DEFAULT_MODE", "codex-cli").strip() or "codex-cli",
        codex_prompt_template=prompt_template,
        service_host=os.getenv("WORKSHOP_SERVICE_HOST", "127.0.0.1"),
        service_port=int(os.getenv("WORKSHOP_SERVICE_PORT", "8000")),
    )
