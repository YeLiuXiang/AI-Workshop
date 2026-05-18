# Ubuntu Migration Guide

This guide keeps the same repository structure and the same `FastAPI + Codex CLI + Python scripts` flow used on Windows.

## 1. Prepare the VM

Use Ubuntu 22.04 LTS or Ubuntu 24.04 LTS.

Install the base packages:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git nginx
```

If Node.js / npm is not already available on the VM, install it first because Codex CLI is installed separately from Python.

## 2. Copy the project

Clone or upload the repo to a fixed path, for example:

```bash
sudo mkdir -p /opt/ai-workshop
sudo chown -R "$USER":"$USER" /opt/ai-workshop
cd /opt/ai-workshop
git clone <your-repo-url>
cd /opt/ai-workshop/AI-Workshop/ppt-generation-enterprise
```

If you are copying from Windows instead of cloning:

- keep the folder name `ppt-generation-enterprise`
- keep `AI picture/`
- keep `content-packs/`
- keep `themes/`
- keep `templates/`

## 3. Create the Python environment

```bash
cd /opt/ai-workshop/AI-Workshop/ppt-generation-enterprise
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Install Codex CLI

Install Codex CLI on Ubuntu and confirm it works:

```bash
codex --version
codex exec --help
```

## 5. Configure authentication

Create the project `.env`:

```bash
cp .env.example .env
```

Recommended first-pass values:

```dotenv
WORKSHOP_PROJECT_ROOT=/opt/ai-workshop/AI-Workshop/ppt-generation-enterprise
WORKSHOP_OUTPUT_ROOT=/opt/ai-workshop/AI-Workshop/ppt-generation-enterprise/workspace
WORKSHOP_JOB_ROOT=/opt/ai-workshop/AI-Workshop/ppt-generation-enterprise/runtime/jobs
WORKSHOP_PYTHON_BIN=/opt/ai-workshop/AI-Workshop/ppt-generation-enterprise/.venv/bin/python
WORKSHOP_DEFAULT_MODE=codex-cli
WORKSHOP_SERVICE_HOST=0.0.0.0
WORKSHOP_SERVICE_PORT=8000

CODEX_CLI_BIN=codex
CODEX_REASONING_EFFORT=low
CODEX_SANDBOX=workspace-write
CODEX_APPROVAL_POLICY=never
CODEX_USE_EPHEMERAL=true
CODEX_IGNORE_USER_CONFIG=false

PPT_ACCENT_IMAGE_DIR=/opt/ai-workshop/AI-Workshop/ppt-generation-enterprise/AI picture
```

Then make sure Codex CLI authentication is available for the Linux user that will run the service.

If Codex CLI depends on `nvm` on Ubuntu, use the wrapper shipped with this repo:

```dotenv
CODEX_CLI_BIN=/home/azureuser/AI-Workshop/ppt-generation-enterprise/deploy/codex-ubuntu-wrapper.sh
```

This avoids relying on interactive shell startup files.

## 6. First local run

Before systemd or Nginx, test the service directly:

```bash
cd /opt/ai-workshop/AI-Workshop/ppt-generation-enterprise
source .venv/bin/activate
./scripts/start_workshop_service.sh
```

In another shell:

```bash
curl http://127.0.0.1:8000/healthz
```

Expected:

- `status: ok`
- `default_mode: codex-cli`
- `output_root` and `project_root` point to the Linux paths

Then open:

```text
http://<vm-ip>/
```

If port `8000` is not exposed publicly, test through SSH tunnel or add Nginx first.

## 7. Configure systemd

Copy the example service:

```bash
sudo cp deploy/workshop-service.service.example /etc/systemd/system/workshop-service.service
sudo systemctl daemon-reload
sudo systemctl enable workshop-service
sudo systemctl start workshop-service
sudo systemctl status workshop-service
```

Useful logs:

```bash
journalctl -u workshop-service -n 100 --no-pager
journalctl -u workshop-service -f
```

## 8. Configure Nginx

Copy the example Nginx site:

```bash
sudo cp deploy/nginx.workshop.conf.example /etc/nginx/sites-available/workshop-service
sudo ln -s /etc/nginx/sites-available/workshop-service /etc/nginx/sites-enabled/workshop-service
sudo nginx -t
sudo systemctl reload nginx
```

If the default site conflicts, disable it:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

## 9. Linux-specific checks

Run these before the workshop:

```bash
test -d "./AI picture" && echo ok
test -x ".venv/bin/python" && echo ok
codex exec --help >/dev/null && echo ok
curl http://127.0.0.1:8000/healthz
```

Also check:

- directory name is `workspace/`, not `Workspace/`
- uploaded files are writable under `runtime/jobs/`
- the service user can read `AI picture/`
- the service user has valid Codex auth

## 10. Suggested rollout path

For the first Ubuntu test, use this order:

1. Start with `WORKSHOP_DEFAULT_MODE=python-fast`
2. Verify `PPT + 手动触发原型` are normal
3. Switch to `WORKSHOP_DEFAULT_MODE=codex-cli`
4. Validate one real form submission with image upload

This reduces variables. If `codex-cli` fails, you still know the web service and Python pipeline are healthy.

## 11. What does not need to change between Windows and Linux

These stay the same:

- frontend page
- FastAPI routes
- workshop JSON schema
- Python generator scripts
- `AI picture/` assets
- `.env` variable names

Only these normally change:

- absolute paths
- Python executable path
- Linux service user
- reverse proxy configuration
- Codex authentication location
