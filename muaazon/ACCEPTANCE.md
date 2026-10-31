# Muaazon CRM AI — Consolidated Acceptance (2026-10-31)
Baseline: Twenty v2.52.0 pinned to commit 62c9c99746abbe3392de76ba77fd32cc93883335.
GitHub fork: https://github.com/sabirshah75/muaazon-crm-ai
Source branch: muaazon/baseline-v1.0
Local runtime: /home/muaazon/projects/muaazon-crm-runtime (outside this repository).
No production deployment or customer data access authorized.

## Verified PASS
- Source checkout preserved, upstream retained and origin configured.
- WSL2/Ubuntu/Docker Engine/Compose functional.
- PostgreSQL and Redis Docker health checks succeeded.
- Twenty server migrated blank test DB, reached healthy status, and served Windows localhost /healthz with HTTP 200.
- Worker initially OOM at 700 MB; increased to 1200 MB and subsequently observed running for 18+ minutes.
- Host port mapped only to 127.0.0.1:3000. DB/Redis have no published host ports.
- Source branding metadata updated (title, social title, manifest), not yet deployed/built.
- Provider-neutral approval-state module written; 5/5 Node tests PASS. All external dispatch remains disabled.

## NOT ACCEPTED / OPEN
- Twenty frontend bundle rebuilt with branding: NOT DONE (monorepo node_modules absent).
- Full Twenty CRM user registration/login and CRUD UX, roles, tenant isolation: NOT TESTED.
- Brand icon/illustrations, responsive design and independent visual QA: NOT DONE.
- Actual AI inference, LeadFlow, Business Agency, Klaviyo, voice, CRM sync adapters: NOT CONNECTED.
- Workflow persistence, schedules, outbound mail/sms, real approval UI: NOT IMPLEMENTED.
- Vendor/API credentials and authorization, data-processing agreements: NOT PROVIDED/VERIFIED.
- Security scanner, dependency vulnerability review, WCAG AA, browser UAT: NOT RUN.
- Backup AND separate-database restore, disaster recovery and rollback: NOT CERTIFIED.
- Long-duration stress, multi-user, failover, resource/power restart: NOT CERTIFIED.
- Compliance: AGPL, MIT and Enterprise file boundaries require review before distributing.
- Windows 10 is outside standard support. Do not expose as production service.
- WSL D: mount warning unresolved.
- C: free disk space around 22 GiB after image pulls. 8 GB system RAM is tight for builds.

## Gating conditions before internal approval
1. Clean package installation and build in an environment with adequate RAM/disk.
2. Full rebranded UI launched and visually accepted.
3. Test users, auth, pipelines, CRUD and authorization checks.
4. Independent review of security/tenant boundaries, secrets and vulnerabilities.
5. Verified provider-specific integration contracts, least privilege, consent and audit logs.
6. Durable approval/outbox execution, retry, idempotency and monitoring.
7. Cross-browser, responsive, accessibility, backup/restore, recovery and documented UAT.
8. Written internal sign-off. No live publishing without authorization.

## Safe local operations
View CRM: http://localhost:3000 (local Windows only).
Run independent integration boundary checks:
  cd /home/muaazon/projects/muaazon-crm-ai && node --test muaazon/tests/*.test.mjs
Stop without deleting volumes:
  sudo docker compose -f /home/muaazon/projects/muaazon-crm-runtime/compose.yaml stop
Do not run docker compose down -v (removes test database).
Never commit the runtime .env, credentials or real client records.
