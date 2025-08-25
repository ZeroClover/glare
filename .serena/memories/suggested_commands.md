Setup
- Create venv: `python3 -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

Run Locally
- Flask dev server (default 5000): `FLASK_APP=main.py python -m flask run`
- Specify port: `FLASK_APP=main.py FLASK_RUN_PORT=5000 python -m flask run`
- Gunicorn (optional): `gunicorn main:app --bind 0.0.0.0:5000`

Quick Checks
- Latest release redirect (inspect headers): `curl -I http://localhost:5000/xtaci/kcptun/linux-amd64`
- Semver‑constrained: `curl -I http://localhost:5000/v2fly/v2ray-core@~v4.27.x/linux-64`
- Invalid regex (expect 400 JSON): `curl -i http://localhost:5000/user/repo/[bad`

Vercel
- Local dev (requires Vercel CLI): `vercel dev`
- Deploy: `vercel` (follow prompts; project uses `vercel.json`)

Maintenance
- Update deps: `pip install -U -r requirements.txt`
- Freeze exact versions (optional): `pip freeze > requirements.txt`

Notes
- No lint/format/test tooling configured in repo. If desired locally:
  - Format with Black: `pip install black && black main.py`
  - Lint with Ruff: `pip install ruff && ruff check .`