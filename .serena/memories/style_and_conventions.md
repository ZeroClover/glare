Code Style & Conventions

General:
- PEP 8 style by convention (not enforced by tools in repo).
- No type hints or docstring standard enforced; keep functions small and readable.
- Keep route logic deterministic and side‑effect free beyond outbound HTTP requests.

API Behavior:
- Single route `/<user>/<repo_ver>/<name_re>`; return either a redirect or a JSON error.
- Validate user input early:
  - Compile `name_re` and return 400 on invalid regex.
  - For semver ranges, use the `node-semver` (`import semver`) compatibility; return 400 on bad ranges, 404 when no tag matches.
- When multiple assets match the regex, choose the shortest filename (existing behavior) to reduce ambiguity.
- Special `name_re` values `tar` and `zip` map to source archive redirects.

HTTP Semantics:
- Use 302 (default Flask `redirect`) for successful matches.
- Use 400 for bad input (regex/semver), 404 for not found, and surface GitHub API status codes when appropriate.

Dependencies:
- `flask` 1.1.x, `requests`, `node-semver` (~=0.7.0 providing the `semver` module)
- Keep dependencies minimal and pin conservatively if adding new ones.

Testing & Verification:
- No automated tests in repo; prefer simple `curl` checks for now.
- Consider rate limits when hitting GitHub unauthenticated; add auth header only if necessary for changes.

Deployment:
- Vercel uses `@vercel/python` with `main.py` as entry; route passthrough for `/.*/.*/.*` to `main.py`.