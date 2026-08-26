# ConsolePythonApp

## Prerequisites

- Python 3.13 or newer
- Docker Desktop, if using the Docker database workflow
- `uv` is recommended for creating the virtual environment and installing packages

`uv` and `venv` work together. The `.venv` directory is the isolated Python environment; `uv` is the tool that can create it and install packages into it. `pip` remains a supported fallback.

## Python environment

Run these commands from the repository root.

### Recommended: uv

Windows PowerShell, macOS, and Linux:

```text
uv venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```text
uv pip install -r requirements.txt
```

If `.venv` already exists, activate it and run the install command again. Do not recreate the environment unless it is damaged.

### Standard-library fallback

If `uv` is not installed, create and activate the environment with Python instead:

```powershell
# Windows PowerShell
py -m venv .venv
.venv\Scripts\Activate
python -m pip install -r requirements.txt
```

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Database configuration

The application reads `DATABASE_URL` from the shell environment when it starts. It does not load `.env` files automatically. Copy `.env.example` to `.env` for reference, but set the variable in your active shell using one of the profiles below.

### Docker PostgreSQL

This is the shared local database configuration. Start only the database service:

```text
docker compose up -d db
```

Use this connection URL from the host Python environment:

```text
postgresql+psycopg://myuser:mysecretpassword@127.0.0.1:5433/mydb
```

Windows PowerShell:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://myuser:mysecretpassword@127.0.0.1:5433/mydb"
```

macOS/Linux:

```bash
export DATABASE_URL="postgresql+psycopg://myuser:mysecretpassword@127.0.0.1:5433/mydb"
```

Check or stop the database:

```text
docker compose ps
docker compose down
```

Use `docker compose down -v` only when you intentionally want to delete the local PostgreSQL volume and its data.

### Native PostgreSQL

Contributors may use a local PostgreSQL installation instead. Create a local database and user according to that installation, then set `DATABASE_URL` to match it.

Windows PowerShell:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://<user>:<password>@127.0.0.1:5432/<database>"
```

macOS/Linux:

```bash
export DATABASE_URL="postgresql+psycopg://<user>:<password>@127.0.0.1:5432/<database>"
```

For Homebrew PostgreSQL on macOS, the service commands are commonly:

```bash
brew services start postgresql
brew services stop postgresql
pg_isready
```

## Automated onboarding

On macOS/Linux, or Windows through WSL or Git Bash, `onboard.sh` automates
environment creation, dependency installation, database configuration, and
API startup:

```bash
./onboard.sh
```

The default profile starts the Docker PostgreSQL service. To use native
PostgreSQL, provide `DATABASE_URL` and select the native profile:

```bash
DATABASE_URL="postgresql+psycopg://<user>:<password>@127.0.0.1:5432/<database>" ./onboard.sh --db native
```

Use `./onboard.sh --no-api` to prepare the environment without starting the
long-running API process. The script uses `uv` when available and falls back
to Python's standard `venv` and `pip` commands.

## Run the API

With the venv active and `DATABASE_URL` set, run this existing command from the repository root:

```text
uvicorn project1.main:app --reload
```

Open the interactive API documentation at <http://127.0.0.1:8000/docs>.

Stop the API with `Ctrl+C`.

## Troubleshooting

- `DATABASE_URL must be set`: set the environment variable in the same terminal session used to start Uvicorn.
- Connection refused on port `5433`: start Docker with `docker compose up -d db` or verify that the native PostgreSQL service is running on its configured port.
- A package is missing: confirm the venv is active, then rerun `uv pip install -r requirements.txt` or `python -m pip install -r requirements.txt`.

## Current scope

Docker Compose provides PostgreSQL only. The FastAPI application runs from the contributor's local Python virtual environment. Package-layout changes, a Dockerfile, and additional test setup are outside this onboarding guide.
