from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from workshop_service.config import Settings


@dataclass
class CodexExecutionResult:
    command: list[str]
    stdout: str
    stderr: str
    returncode: int


class CodexCliRunner:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def run(
        self,
        prompt: str,
        workdir: Path,
        image_paths: list[Path],
        timeout_seconds: int,
    ) -> CodexExecutionResult:
        command: list[str] = [
            self.settings.codex_cli_bin,
            "-C",
            str(workdir),
            "--ask-for-approval",
            self.settings.codex_approval_policy,
            "--sandbox",
            self.settings.codex_sandbox,
        ]
        if self.settings.codex_reasoning_effort:
            command.extend(
                ["-c", f'model_reasoning_effort="{self.settings.codex_reasoning_effort}"']
            )

        command.append("exec")

        if self.settings.codex_use_ephemeral:
            command.append("--ephemeral")
        if self.settings.codex_ignore_user_config:
            command.append("--ignore-user-config")
        if self.settings.codex_skip_git_repo_check:
            command.append("--skip-git-repo-check")
        if self.settings.codex_model:
            command.extend(["--model", self.settings.codex_model])
        if image_paths:
            command.extend(["-i", *[str(path) for path in image_paths]])

        command.append(prompt)

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
            timeout=timeout_seconds,
            cwd=workdir,
            env={
                **os.environ,
                "PYTHONIOENCODING": "utf-8",
            },
            shell=False,
        )
        return CodexExecutionResult(
            command=command,
            stdout=completed.stdout,
            stderr=completed.stderr,
            returncode=completed.returncode,
        )
