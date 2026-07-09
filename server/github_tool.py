"""GitHub 관련 정보 조회 도구"""

import json
import os
import urllib.request
from urllib.error import HTTPError, URLError
from typing import Optional


def _build_headers() -> dict:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Portfolio-App"
    }
    token = os.getenv("GITHUB_API_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def _fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers=_build_headers())
    with urllib.request.urlopen(request, timeout=10) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw)


def get_repository_info(repo: Optional[str] = None) -> dict:
    repo = repo or os.getenv("GITHUB_REPO")
    if not repo:
        raise ValueError("GITHUB_REPO 환경변수가 설정되어 있지 않습니다.")

    url = f"https://api.github.com/repos/{repo}"
    try:
        data = _fetch_json(url)
    except HTTPError as exc:
        raise RuntimeError(f"GitHub API 요청 실패: {exc.code} {exc.reason}")
    except URLError as exc:
        raise RuntimeError(f"GitHub API 요청 실패: {exc.reason}")

    return {
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "html_url": data.get("html_url"),
        "stargazers_count": data.get("stargazers_count", 0),
        "forks_count": data.get("forks_count", 0),
        "open_issues_count": data.get("open_issues_count", 0),
        "watchers_count": data.get("watchers_count", 0),
        "language": data.get("language"),
        "license": data.get("license", {}).get("name") if data.get("license") else None,
        "updated_at": data.get("updated_at")
    }
