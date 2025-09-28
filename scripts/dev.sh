#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

compose() { docker compose -f infra/compose.dev.yml "$@"; }

case "${1:-}" in
  up)         compose up -d --build ;;
  down)       compose down ;;
  logs)       compose logs -f --tail=200 backend ;;
  lint)       compose exec backend ruff check . && echo "Ruff: OK" ;;
  format)     compose exec backend bash -lc "ruff check --select I --fix . && black . && isort ." ;;
  migrate)    compose exec backend python manage.py migrate ;;
  shell)      compose exec -it backend bash ;;
  createsu)   compose exec -it backend python manage.py createsuperuser ;;
  *) echo "Usage: scripts/dev.sh {up|down|logs|lint|format|migrate|shell|createsu}"; exit 2 ;;
esac
