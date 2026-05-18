#!/usr/bin/env bash
set -euo pipefail

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ -s "${NVM_DIR}/nvm.sh" ]]; then
  # shellcheck disable=SC1090
  . "${NVM_DIR}/nvm.sh"
  if command -v nvm >/dev/null 2>&1; then
    nvm use default >/dev/null 2>&1 || true
  fi
fi

export PATH="$HOME/.nvm/versions/node/v20.20.2/bin:$HOME/.local/bin:$PATH"
exec "$HOME/.nvm/versions/node/v20.20.2/bin/codex" "$@"
