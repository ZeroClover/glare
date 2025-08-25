Project: Glare

Purpose:
- Redirects to GitHub release asset URLs based on a regex match and an optional exact tag or npm‑style semver range.
- Useful for Dockerfiles/CI where the desired asset name varies but follows a predictable pattern.

Tech Stack:
- Language: Python (Flask app for Vercel’s Python runtime)
- Framework/libs: Flask, requests, node-semver (exposes the `semver` module)
- Hosting: Vercel (see `vercel.json`)
- External API: GitHub REST API `/repos/{owner}/{repo}/releases` and release endpoints

Entrypoint & Routing:
- Entrypoint module: `main.py` exporting `app`
- Route: `/<user>/<repo_ver>/<name_re>` where `repo_ver` is `{repo}` or `{repo}@{tag|semver}` and `name_re` is a regex, or special values `tar`/`zip` for source archives.
- Behavior:
  - If `@{tag}` present: exact match; if not found, treat post-`@` as semver range and choose the highest satisfying tag.
  - If `tar`/`zip`: redirect to tarball/zipball URLs.
  - Else: match assets by regex, pick the shortest name when multiple match, then 302 redirect.
  - Errors are JSON with appropriate HTTP status.

Repo Structure (top-level):
- `main.py`: Flask handler and GitHub API logic
- `requirements.txt`: Flask, requests, node-semver
- `vercel.json`: Vercel build and route config
- `README.md`: Usage, motivation, examples

Notable Conventions:
- No type hints or test suite present.
- Error responses through `flask.jsonify` with status codes 4xx on client issues and GitHub API errors surfaced pass‑through.

Examples:
- Latest: `/xtaci/kcptun/linux-amd64`
- With semver: `/v2fly/v2ray-core@~v4.27.x/linux-64`