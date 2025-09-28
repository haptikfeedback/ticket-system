#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

COMPOSE_FILE="${COMPOSE_FILE:-$(ls infra/compose.dev.y* | head -n1)}"
compose() { docker compose -f "$COMPOSE_FILE" "$@"; }

case "${1:-}" in
  up)         compose up -d --build ;;
  down)       compose down ;;
  logs)       compose logs -f --tail=200 backend ;;
  lint)       compose exec backend ruff check . && echo "Ruff: OK" ;;
  format)     compose exec backend bash -lc "ruff check --select I --fix . && black . && isort ." ;;
  migrate)    compose exec backend python manage.py migrate ;;
  shell)      compose exec -it backend bash ;;
  createsu)   compose exec -it backend python manage.py createsuperuser ;;
  schema:yaml)
              mkdir -p docs/api
              compose exec backend python manage.py spectacular --file docs/api/openapi.yaml
              ;;
  schema:json)
              mkdir -p docs/api
              compose exec backend python manage.py spectacular --format openapi-json --file docs/api/openapi.json
              ;;
  schema:diff)
              mkdir -p docs/api
              compose exec backend bash -lc "python manage.py spectacular --file docs/api/_new.yaml"
              diff -u docs/api/openapi.yaml docs/api/_new.yaml || true
              ;;
  *) echo "Usage: scripts/dev.sh {up|down|logs|lint|format|migrate|shell|createsu|schema:yaml|schema:json|schema:diff}"; exit 2 ;;
esac
