#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DATABASE_PROFILE="${DATABASE_PROFILE:-docker}"
START_API=true

usage() {
    cat <<'EOF'
Usage: ./onboard.sh [options]

Set up the local Python environment, configure the database, and start the API.

Options:
  --db docker     Use the Docker Compose PostgreSQL service (default)
  --db native     Use DATABASE_URL from the current shell
  --no-api        Complete setup without starting Uvicorn
  -h, --help      Show this help

Examples:
  ./onboard.sh
  ./onboard.sh --db native
  DATABASE_URL='postgresql+psycopg://user:password@127.0.0.1:5432/database' ./onboard.sh --db native
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --db)
            [[ $# -ge 2 ]] || { echo "Missing database profile after --db" >&2; exit 2; }
            DATABASE_PROFILE="$2"
            shift 2
            ;;
        --no-api)
            START_API=false
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

case "$DATABASE_PROFILE" in
    docker)
        command -v docker >/dev/null 2>&1 || { echo "Docker is required for the docker database profile." >&2; exit 1; }
        docker compose up -d db
        export DATABASE_URL="${DATABASE_URL:-postgresql+psycopg://myuser:mysecretpassword@127.0.0.1:5433/mydb}"
        ;;
    native)
        if [[ -z "${DATABASE_URL:-}" ]]; then
            echo "DATABASE_URL must be set when using the native database profile." >&2
            exit 1
        fi
        ;;
    *)
        echo "Database profile must be 'docker' or 'native'." >&2
        exit 2
        ;;
esac

if [[ ! -d .venv ]]; then
    if command -v uv >/dev/null 2>&1; then
        uv venv .venv
    else
        command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required." >&2; exit 1; }
        python3 -m venv .venv
    fi
fi

if [[ -x .venv/bin/python ]]; then
    VENV_PYTHON=".venv/bin/python"
elif [[ -x .venv/Scripts/python.exe ]]; then
    VENV_PYTHON=".venv/Scripts/python.exe"
else
    echo "Could not find the Python executable inside .venv." >&2
    exit 1
fi

if command -v uv >/dev/null 2>&1; then
    uv pip install --python "$VENV_PYTHON" -r requirements.txt
else
    "$VENV_PYTHON" -m pip install -r requirements.txt
fi

if [[ "$START_API" == true ]]; then
    export DATABASE_URL
    exec "$VENV_PYTHON" -m uvicorn project1.main:app --reload
fi

echo "Setup complete. DATABASE_URL is configured for this script's shell only."
echo "Start the API with: $VENV_PYTHON -m uvicorn project1.main:app --reload"
