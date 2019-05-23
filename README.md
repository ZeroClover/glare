# Glare

[![Deploy to now](https://deploy.now.sh/static/button.svg)](https://deploy.now.sh/?repo=https://github.com/Contextualist/glare)

A little service for you to **g**et **la**test **re**leases from GitHub gracefully. Simply make a get request to Glare with the repo name and release file name regex, and she will lead you to the way.

### Demo
The following will redirect you to `https://github.com/xtaci/kcptun/releases/download/{latest_version_tag}/kcptun-linux-amd64-{latest_version_number}.tar.gz`, and download the latest release of kcptun for linux-amd64. 
```bash
curl -fLO https://glare.now.sh/xtaci/kcptun/linux-amd64
```

## Motivation
Sometimes when I'm writing a Dockerfile, I need to install packages from their GitHub latest releases. A neat way is to parse JSON responses from GitHub API with [`jq`](https://stedolan.github.io/jq) and get the desire link. Such way requires downlaoding `jq` from GitHub (The binary from Alpine apk is lack of regex feature). Still, the expression with `jq` is not clear enough, and parsing JSON with `sed` is way dirtier. So I spend a little time to write Glare. I hope she will save you a few minutes or from a frustring moment.

## Usage
```
/{owner}/{repo}/{file_name_regex}
```
`{file_name_regex}` is a regular expression to match the file (or specially, it can be `tar` or `zip` standing for the source code download in the respective format). It should match at least one file among the latest release files, otherwise Glare will throw an error. If multiple files are matched, Glare returns the one with shortest length.

Tip: to check if a request leads to the desired redirection, `curl` it without any option.

## Docker (legacy version)
See branch [`docker`](https://github.com/Contextualist/glare/tree/docker)
