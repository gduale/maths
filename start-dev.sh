#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [[ ! -x .venv/bin/python ]]; then
    printf '%s\n' "Environnement Python manquant. Exécute :" \
        "uv venv --python 3.14 .venv" \
        "uv pip install --python .venv/bin/python -r requirements.txt" >&2
    exit 1
fi

if ! .venv/bin/python -c 'import django' 2>/dev/null; then
    printf '%s\n' "Django est manquant. Exécute :" \
        "uv pip install --python .venv/bin/python -r requirements.txt" >&2
    exit 1
fi

.venv/bin/python manage.py migrate --noinput
printf '\n%s\n' "Application : http://localhost:8000" "Pour arrêter : Ctrl+C"
exec .venv/bin/python manage.py runserver 127.0.0.1:8000
