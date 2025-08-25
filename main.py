from flask import Flask, jsonify, redirect
import requests
import semver
import re
from typing import Optional, Dict, Any, List

app = Flask(__name__)

@app.route('/<user>/<repo_ver>/<name_re>')
def get_release(user, repo_ver, name_re):
    try:
        name_reobj = re.compile(name_re)
    except re.error as e:
        return jsonify(message=f"bad regular expression: {e.msg}"), 400

    repo_ver = repo_ver.split('@', 1)
    repo = repo_ver[0]
    release_obj = None
    if len(repo_ver) == 2:  # versioned
        ver = repo_ver[1]
        # Special selector: latest pre-release
        if ver.lower() in ("pre-release", "prerelease"):
            all_releases, err = api_req(f"https://api.github.com/repos/{user}/{repo}/releases")
            if err:
                return err
            pre = latest_prerelease(all_releases)
            if pre is None:
                return jsonify(message="no pre-release found"), 404
            release_obj = pre
            tag = None
        else:
            all_releases, err = api_req(f"https://api.github.com/repos/{user}/{repo}/releases")
            if err:
                return err
            all_tags = [x['tag_name'] for x in all_releases]
            if ver in all_tags:  # exact match
                tag = f"tags/{ver}"
            else:
                try:
                    v = semver.max_satisfying(all_tags, ver)
                except Exception as e:
                    return jsonify(message=f"error matching the tag: {e}"), 400
                if v is None:
                    return jsonify(message="no tag matched"), 404
                tag = f"tags/{v}"
    else:
        tag = "latest"

    if release_obj is None:
        release, err = api_req(f"https://api.github.com/repos/{user}/{repo}/releases/{tag}")
        if err:
            return err
    else:
        release = release_obj

    if name_re == 'tar':
        return redirect(release['tarball_url'])
    if name_re == 'zip':
        return redirect(release['zipball_url'])
    assets = release['assets']
    matched = [x['browser_download_url'] for x in assets if name_reobj.search(x['name'])]
    if len(matched) == 0:
        return jsonify(message="no file matched"), 404
    matched.sort(key=len)
    return redirect(matched[0])

def api_req(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return None, (jsonify(message="error from GitHub API",
                              github_api_msg=resp.json()), resp.status_code)
    return resp.json(), None


def latest_prerelease(releases: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Return the newest published pre-release (non-draft), or None if absent."""
    candidates = [
        r for r in releases
        if r.get("prerelease") and not r.get("draft")
    ]
    if not candidates:
        return None
    # Prefer published_at, fallback to created_at
    def ts(r: Dict[str, Any]) -> str:
        return r.get("published_at") or r.get("created_at") or ""

    candidates.sort(key=ts, reverse=True)
    return candidates[0]
