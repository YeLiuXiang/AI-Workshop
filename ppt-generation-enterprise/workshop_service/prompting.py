from __future__ import annotations

from pathlib import Path


def build_codex_prompt(
    template_path: Path,
    request_path: Path,
    scenario_output_path: Path,
    image_paths: list[Path],
) -> str:
    template = template_path.read_text(encoding="utf-8")
    image_section = "\n".join(f"- {path.as_posix()}" for path in image_paths) or "- 无"
    return (
        template.replace("{request_path}", request_path.as_posix())
        .replace("{scenario_output_path}", scenario_output_path.as_posix())
        .replace("{image_paths}", image_section)
    )
