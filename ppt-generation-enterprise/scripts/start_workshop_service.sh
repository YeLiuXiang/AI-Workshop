#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"
if [[ -x "${PROJECT_ROOT}/.venv/bin/python" ]]; then
  "${PROJECT_ROOT}/.venv/bin/python" -m workshop_service
else
  python -m workshop_service
fi
