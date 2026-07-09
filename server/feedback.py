"""피드백 저장 모듈"""

import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "feedback.json"


def _ensure_file() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_feedback() -> list[dict]:
    _ensure_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_feedback(entries: list[dict]) -> None:
    _ensure_file()
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def add_feedback(name: str, rating: int, comment: str) -> dict:
    name = name.strip()
    comment = comment.strip()
    if not name or not comment:
        raise ValueError("이름과 코멘트를 모두 입력해야 합니다.")
    if rating < 1 or rating > 5:
        raise ValueError("rating은 1에서 5 사이여야 합니다.")

    feedback = {
        "name": name,
        "rating": rating,
        "comment": comment,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    entries = load_feedback()
    entries.insert(0, feedback)
    save_feedback(entries)
    return feedback


def get_recent_feedback(limit: int = 20) -> list[dict]:
    return load_feedback()[:limit]


def get_feedback_stats() -> dict:
    entries = load_feedback()
    if not entries:
        return {"count": 0, "average_rating": 0.0}
    total = sum(entry.get("rating", 0) for entry in entries)
    return {"count": len(entries), "average_rating": total / len(entries)}
