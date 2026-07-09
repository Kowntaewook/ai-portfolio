"""
프로젝트 조회수 / 좋아요 저장 모듈
"""

import json
from collections import defaultdict
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "project_stats.json"


def _ensure_file() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({"views": {}, "likes": {}, "liked_users": {}}), encoding="utf-8")


def load_stats() -> dict:
    _ensure_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"views": {}, "likes": {}, "liked_users": {}}


def save_stats(stats: dict) -> None:
    _ensure_file()
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def increment_view(project_id: str) -> dict:
    stats = load_stats()
    stats.setdefault("views", {})
    stats["views"][project_id] = stats["views"].get(project_id, 0) + 1
    save_stats(stats)
    return stats["views"]


def toggle_like(project_id: str, user_id: str) -> dict:
    if not user_id:
        raise ValueError("user_id가 필요합니다.")

    stats = load_stats()
    stats.setdefault("views", {})
    stats.setdefault("likes", {})
    stats.setdefault("liked_users", {})

    liked_users = set(stats["liked_users"].get(project_id, []))
    if user_id in liked_users:
        liked_users.remove(user_id)
        stats["likes"][project_id] = max(0, stats["likes"].get(project_id, 0) - 1)
        liked = False
    else:
        liked_users.add(user_id)
        stats["likes"][project_id] = stats["likes"].get(project_id, 0) + 1
        liked = True

    stats["liked_users"][project_id] = list(liked_users)
    save_stats(stats)

    return {
        "liked": liked,
        "views": stats["views"].get(project_id, 0),
        "likes": stats["likes"].get(project_id, 0)
    }


def get_stats(project_id: str) -> dict:
    stats = load_stats()
    return {
        "views": stats.get("views", {}).get(project_id, 0),
        "likes": stats.get("likes", {}).get(project_id, 0),
        "liked": False
    }


def get_all_stats() -> dict:
    stats = load_stats()
    return {
        "views": stats.get("views", {}),
        "likes": stats.get("likes", {}),
        "liked_users": stats.get("liked_users", {})
    }


def get_popular_projects(limit: int = 5) -> list[dict]:
    stats = load_stats()
    likes = stats.get("likes", {})
    sorted_projects = sorted(likes.items(), key=lambda x: x[1], reverse=True)
    return [{"project_id": project_id, "likes": count} for project_id, count in sorted_projects[:limit]]
