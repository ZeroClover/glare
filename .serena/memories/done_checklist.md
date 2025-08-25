Before You Finish a Change

- Run locally and sanity‑check with sample `curl` requests.
- Verify error cases (bad regex, no matching tag, no asset match).
- Confirm GitHub API responses are handled (status != 200) and user‑visible messages are clear.
- Ensure `requirements.txt` is updated if dependencies changed.
- Keep API behavior backward‑compatible (route shape and semantics).
- Update `README.md` if usage or examples change.
- If deployment is used, run `vercel dev` locally to validate routing, then `vercel` to deploy.
- Keep code simple; avoid adding global state or side effects.

Optional (local hygiene)
- Format/Lint if you use local tools (e.g., Black/Ruff).
- Consider adding minimal tests if functionality grows.