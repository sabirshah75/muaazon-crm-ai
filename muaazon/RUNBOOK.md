# Muaazon CRM AI — Local Engineering Runbook

## Location and safety
- GitHub: https://github.com/sabirshah75/muaazon-crm-ai
- Source: /home/muaazon/projects/muaazon-crm-ai
- Branch: muaazon/baseline-v1.0 (tracks origin)
- Isolated compose runtime: /home/muaazon/projects/muaazon-crm-runtime
- Local-only CRM: http://localhost:3000/welcome
- Never publish port 3000 to a public interface; database and Redis have no host ports.
- Secrets are held outside Git in runtime/.env (0600). Never commit or print that file.
- AGPL/MIT/Enterprise licensing boundaries must be reviewed for distribution.
- The running frontend is released Twenty v2.52.0, with only a read-only branding/a11y HTML overlay.

## Routine operations (Ubuntu WSL)
Start all services:
  sudo docker compose -f /home/muaazon/projects/muaazon-crm-runtime/compose.yaml up -d
Check:
  sudo docker compose -f /home/muaazon/projects/muaazon-crm-runtime/compose.yaml ps
  curl -fsS http://localhost:3000/healthz
Stop without losing data:
  sudo docker compose -f /home/muaazon/projects/muaazon-crm-runtime/compose.yaml stop
Never run 'down -v' without explicit approval.

## Safe offline test suite
  cd /home/muaazon/projects/muaazon-crm-ai
  node --test muaazon/tests/*.test.mjs
  python3 -m unittest discover -s muaazon/tests -p test_brand_runtime.py -v
  python3 muaazon/tools/security_smoke.py
  git diff --check

Windows browser QA (requires the isolated MuaazonCRM qa-venv):
  $qa = Join-Path $env:LOCALAPPDATA 'MuaazonCRM\qa-venv'
  $env:MUA_QA_DIR = Join-Path $env:LOCALAPPDATA 'MuaazonCRM\qa-evidence'
  & "$qa\Scripts\python.exe" '\\wsl.localhost\Ubuntu-24.04\home\muaazon\projects\muaazon-crm-ai\muaazon\tools\browser_smoke.py'
  $env:MUA_AXE_JS = Join-Path $env:LOCALAPPDATA 'MuaazonCRM\qa-tools\node_modules\axe-core\axe.min.js'
  & "$qa\Scripts\python.exe" '\\wsl.localhost\Ubuntu-24.04\home\muaazon\projects\muaazon-crm-ai\muaazon\tools\axe_audit.py'

## Metadata overlay (reproducible)
The base compiled frontend is captured separately under runtime/frontend/base.
Rebuild only the overlay:
  python3 /home/muaazon/projects/muaazon-crm-ai/muaazon/tools/brand_runtime.py --base /home/muaazon/projects/muaazon-crm-runtime/frontend/base --output /home/muaazon/projects/muaazon-crm-runtime/frontend/overlay
Restart only the local server to flush cached HTML:
  sudo docker restart muaazon-crm-ai-server-1
Startup may require resource-limited migration checks; wait for a healthy status.
The overlay is a compatibility measure, not a full branded frontend build.

## Database backup and restore acceptance
Only while both user and workspace tables are empty:
  sudo bash /home/muaazon/projects/muaazon-crm-ai/muaazon/tools/verify_backup_restore.sh
It restores to a new temporary DB, compares table counts and removes test artifacts.
Production backup schedules, encrypted off-device retention and RPO/RTO need separate approval.

## Explicitly not yet certified
Real CRM user creation, CRUD, roles/tenant isolation, external providers, actual AI inference,
durable workflow queue, frontend build, complete premium branding, independent security,
manual accessibility, full browser UAT, and production deployment.
