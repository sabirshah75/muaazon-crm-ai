#!/usr/bin/env bash
set -euo pipefail
# Only for a local empty QA database, never automatically for production/customer data.
container="muaazon-crm-ai-db-1"
scratch="muaazon_restore_qa"
backup="/tmp/muaazon-backup-restore-qa.dump"
run() { docker exec "$container" "$@"; }
cleanup() {
  run dropdb -U postgres --if-exists "$scratch" >/dev/null 2>&1 || true
  run rm -f "$backup" >/dev/null 2>&1 || true
}
trap cleanup EXIT
workspaces="$(run psql -U postgres -d default -Atqc 'SELECT COUNT(*) FROM core."workspace"')"
users="$(run psql -U postgres -d default -Atqc 'SELECT COUNT(*) FROM core."user"')"
if [[ "$workspaces" != "0" || "$users" != "0" ]]; then
  echo "STOP: existing workspaces/users found. Refusing non-empty QA backup." >&2
  exit 4
fi
if run psql -U postgres -d postgres -Atqc "SELECT 1 FROM pg_database WHERE datname='$scratch'" | grep -q 1; then
  echo "STOP: temporary database already exists; refusing overwrite" >&2
  exit 5
fi
run pg_dump -U postgres -d default --format=custom -f "$backup"
run createdb -U postgres "$scratch"
run pg_restore -U postgres --exit-on-error --no-owner --no-privileges -d "$scratch" "$backup"
source_tables="$(run psql -U postgres -d default -Atqc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema IN ('core','public')")"
restored_tables="$(run psql -U postgres -d "$scratch" -Atqc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema IN ('core','public')")"
test "$source_tables" -gt 0
test "$source_tables" = "$restored_tables"
echo "BACKUP_RESTORE_PASS tables=$restored_tables workspaces=$workspaces users=$users"
