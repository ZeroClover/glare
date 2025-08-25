# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Glare is a Flask-based web service that provides graceful downloads of GitHub releases. It acts as a proxy service that resolves release URLs from GitHub API and redirects users to the appropriate download links, with support for version constraints and file name pattern matching.

## Architecture

- **Single Flask application** (`main.py`) - Contains the entire web service logic
- **Core functionality**: Single route handler `get_release()` at main.py:8 that processes requests in format `/{owner}/{repo}[@{version}]/{file_regex}`
- **Version resolution**: Uses semver matching via `node-semver` library for flexible version constraints
- **GitHub API integration**: Direct API calls to fetch release information without authentication
- **Deployment**: Configured for Vercel serverless deployment via `vercel.json`

## Key Components

### Route Handler (main.py:8-47)
- Parses repository, version constraints, and file matching patterns
- Handles exact version matching and semver range matching
- Returns redirects to GitHub download URLs or source archives

### API Integration (main.py:49-54) 
- `api_req()` function handles GitHub API requests with error handling
- No authentication required - uses public GitHub API endpoints

## Development Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
python main.py
# or
flask run
```

### Testing
Test the service by making GET requests:
```bash
# Test latest release
curl -I https://localhost:5000/xtaci/kcptun/linux-amd64

# Test version constraint
curl -I https://localhost:5000/v2fly/v2ray-core@~v4.27.x/linux-64
```

## Dependencies

- `flask~=1.1.4` - Web framework
- `requests` - HTTP client for GitHub API
- `node-semver~=0.7.0` - Semantic version matching

## Deployment

Configured for Vercel deployment with Python runtime. The `vercel.json` routes all matching patterns to `main.py`.