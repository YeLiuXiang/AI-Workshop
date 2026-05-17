# Workshop Codex Service Design

## Goal

Add a cross-platform service layer around the existing workshop generation pipeline so the same project can:

- run on Windows with local Codex CLI
- migrate later to Linux VM with minimal code changes
- preserve the existing Python PPT/document generation path
- optionally let Codex CLI handle scenario normalization before the Python pipeline runs

## Scope

This phase does not rewrite the existing workshop scripts. It adds:

- a `FastAPI` service entrypoint
- a file-based job runner
- a Codex CLI adapter built around `codex exec`
- environment-based configuration
- deployment notes and dependency manifest

## Runtime Modes

### 1. Python fast path

The request payload is saved as input JSON and passed directly to:

`python scripts/generate_workshop_package.py --fast`

Use this when the input is already structured enough and workshop stability matters most.

### 2. Codex CLI normalization path

The request payload and uploaded images are saved into a per-job directory.
The service then invokes Codex CLI in non-interactive mode to create a normalized scenario JSON file.
That normalized file is then passed to the existing workshop package generator.

This keeps the orchestration boundary explicit:

- Codex CLI handles flexible reasoning and normalization
- Python scripts handle deterministic artifact generation

## Cross-Platform Rules

- Do not rely on Windows absolute paths.
- Resolve all runtime paths from the repository root or environment variables.
- Use subprocess argument lists instead of shell-built command strings.
- Keep generated job files inside the repo workspace so Codex CLI can access them under both Windows and Linux.

## Initial API

- `GET /healthz`
- `POST /api/jobs/json`
- `POST /api/jobs/form`
- `GET /api/jobs/{job_id}`
- `GET /api/jobs/{job_id}/artifacts`
- `GET /api/jobs/{job_id}/artifacts/{artifact_name}`

## Key Environment Variables

- `WORKSHOP_PROJECT_ROOT`
- `WORKSHOP_OUTPUT_ROOT`
- `WORKSHOP_JOB_ROOT`
- `WORKSHOP_DEFAULT_MODE`
- `CODEX_CLI_BIN`
- `CODEX_MODEL`
- `CODEX_SANDBOX`
- `CODEX_APPROVAL_POLICY`
- `CODEX_USE_EPHEMERAL`
- `PPT_ACCENT_IMAGE_DIR`

## First Implementation Boundary

This round should stop at:

- backend service runs locally
- job state persists to disk
- Codex CLI invocation is configurable
- existing script output can be downloaded through the service

Prototype HTML generation can be added later as another job stage.
