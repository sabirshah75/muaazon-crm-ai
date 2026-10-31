# Muaazon CRM AI — Consolidated Engineering Acceptance, 31 October 2026

## Source and deployment
Fork: https://github.com/sabirshah75/muaazon-crm-ai
Upstream: https://github.com/twentyhq/twenty
Baseline release: twenty/v2.52.0 (62c9c99746abbe3392de76ba77fd32cc93883335)
Source checkout: /home/muaazon/projects/muaazon-crm-ai
Isolated runtime: /home/muaazon/projects/muaazon-crm-runtime
Local URL: http://localhost:3000/welcome (not publicly reachable)
IMPORTANT: only the released frontend + minimal HTML/CSS/a11y overlay is deployed. The React source edits have NOT been compiled into a new frontend build.

## PASS: verified execution
- GitHub fork and local origin/upstream branch tracking verified previously.
- Ubuntu 24.04 LTS WSL2, Docker Engine/Compose available.
- PostgreSQL 16 + Redis local Docker healthchecks successful.
- Twenty v2.52.0 server successfully migrated test database, became healthy and served HTTP 200 from Windows.
- Worker previously ran 28+ minutes; after temporary QA stop it was restarted and was running with no OOM at immediate check.
- Only 127.0.0.1:3000 published; DB/Redis not published on host.
- Compiled frontend served Muaazon CRM AI title and matching PWA manifest in Windows.
- Root and health endpoints HTTP 200.
- Playwright native Chrome welcome-screen smoke: desktop 1365x768 and mobile 390x844 both PASS, no JS page errors, no horizontal overflow.
- Chrome clicked Continue with Email and revealed form; no browser JS errors.
- Synthetic-only registration navigation reached the real Sign up form with Email and Password fields; no fake initial administrator was registered.
- First axe-core WCAG A/AA audit found 2 serious violations on desktop and mobile: low-contrast legal links and unlabelled logo link.
- Targeted React source changes + runtime compatibility overlay made; second axe audit found ZERO automatically detected violations on both screens, with ONE incomplete/manual-check item per screen.
- Node integration approval/draft tests: 5 passed, 0 failed.
- Node provider-neutral AI draft adapter tests: 7 passed, 0 failed (mock transport, no live inference).
- Python branding overlay unit tests: 2 passed, 0 failed.
- HTTP loopback security smoke PASS: CSP, X-Content-Type-Options nosniff, X-Frame-Options SAMEORIGIN, no secrets in served HTML, anonymous query returned no current-user data.
- Secrets file outside Git has Unix mode 0600.
- Empty test database backed up in PostgreSQL custom format, restored into an isolated temporary database: 76/76 tables matched; no users/workspaces. Scratch DB removed.

## NOT ACCEPTED / REMAINING PRODUCT WORK
1. Full premium Muaazon UI branding: logo/icon/navigation/16-screen-level customization not done. Frontend must be rebuilt to deploy React source changes.
2. Real first user registration, actual authentication, contacts/companies/deals pipeline CRUD, role permissions, multi-workspace isolation and admin UAT: not done. Current QA database has no users/workspaces.
3. Model-driven AI: adapter has mock-based unit tests; no authorized live model provider configured or tested. Local LiteLLM ports 4020 and 4021 were closed at verification.
4. LeadFlow AI, Agency, Klaviyo, calendars/voice/marketing integrations: no active provider sync or certified integration contracts. The outbox/approval boundary remains disconnected from Twenty's application platform; external sending is intentionally disabled.
5. Durable jobs, end-to-end idempotency, persistence, retries, alerting, production workflows: not implemented.
6. Security: automated smoke only; full vulnerability/dependency scanning, tenant isolation attack testing and qualified independent security review remain.
7. Accessibility: automated axe passes on only the welcome screen; manual keyboard, screen-reader, full app navigation and independent WCAG 2.2 AA signoff remain.
8. Multi-browser functional regression, load tests, true disaster-recovery RPO/RTO, encrypted off-device backup policy, independent customer UAT, release decision and publishing remain.
9. WSL D: automount warning remains; Windows 10 and 8 GB RAM/limited C: disk are insufficient for confident local production hosting.
10. License: preserve Twenty AGPL/MIT and Enterprise-licensed file restrictions; legal clearance before distribution.

## Release decision
LOCAL FOUNDATION / RECOVERY / WELCOME SCREEN SMOKE: PASS.
FULL COMMERCIAL APPLICATION / LIVE INTEGRATIONS / SECURITY / PUBLIC RELEASE: FAIL (not implemented or unverified).
Do not process real customers, publicize this service, or claim external provider integration is live.

## Evidence / reproduction
Source tools: muaazon/tools/
Node tests: node --test muaazon/tests/*.test.mjs
Python tests: python3 -m unittest discover -s muaazon/tests -p test_brand_runtime.py -v
Chrome evidence on Windows: %LOCALAPPDATA%\MuaazonCRM\qa-evidence\
Runtime-only overlay: /home/muaazon/projects/muaazon-crm-runtime/frontend/overlay
Source runbook: muaazon/RUNBOOK.md
