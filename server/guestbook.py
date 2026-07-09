"""
방명록 저장 모듈
"""

import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "guestbook.json"


def _ensure_file() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_guestbook() -> list[dict]:
    _ensure_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_guestbook(entries: list[dict]) -> None:
    _ensure_file()
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def add_guestbook_entry(name: str, message: str) -> dict:
    name = name.strip()
    message = message.strip()
    if not name or not message:
        raise ValueError("이름과 메시지를 모두 입력해야 합니다.")

    entry = {
        "name": name,
        "message": message,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    entries = load_guestbook()
    entries.insert(0, entry)
    save_guestbook(entries)
    return entry


def get_recent_guestbook(limit: int = 20) -> list[dict]:
    return load_guestbook()[:limit]
