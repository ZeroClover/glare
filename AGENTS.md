# Repository Guidelines

## Project Structure & Module Organization
- `main.py`: Flask app and single route that resolves GitHub releases (exact tag or semver) and redirects to an asset by regex.
- `requirements.txt`: Python dependencies (Flask, requests, node-semver).
- `vercel.json`: Vercel build and routing to `main.py`.
- `README.md`: Usage and examples. `.serena/`: agent configuration (do not change unless updating tooling).
- No `tests/` directory yet.

## Build, Test, and Development Commands
- Create env and install: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Run locally: `FLASK_APP=main.py python -m flask run` (dev server) or `gunicorn main:app --bind 0.0.0.0:5000`.
- Quick check: `curl -I http://localhost:5000/xtaci/kcptun/linux-amd64` (expect 302 redirect).
- Vercel: `vercel dev` to emulate routing; `vercel` to deploy.

## Coding Style & Naming Conventions
- Python, PEP 8, 4‑space indentation, `snake_case` for functions/variables.
- Keep handler logic small with early returns; keep responses JSON for errors, 302 for redirects.
- Optional local tooling: Black (`black main.py`) and Ruff (`ruff check .`). No type hints required.

## Testing Guidelines
- No test framework in repo. Preferred: `pytest` with files under `tests/test_*.py`.
- Cover cases: invalid regex (400), no semver/tag match (404), no asset match (404), tar/zip shortcuts (302), regex match (302 shortest).
- If added: run with `pytest -q`. No coverage threshold enforced.

## Commit & Pull Request Guidelines
- History shows short, imperative subjects; occasional Conventional Commits (`fix: …`, `documentation: …`). Prefer Conventional Commits when possible.
- PRs: include summary, reasoning, steps to reproduce/verify (example `curl`), and link issues. For behavior changes, include before/after headers or screenshots of curl output.

## Security & Configuration Tips
- GitHub API is unauthenticated and rate‑limited. If adding authentication, use an env var (e.g., `GITHUB_TOKEN`) configured in Vercel; never hard‑code secrets.
- Avoid logging tokens or full API responses; log minimal context and status codes.
