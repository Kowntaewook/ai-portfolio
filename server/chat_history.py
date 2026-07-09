"""챗 히스토리 저장 모듈"""

import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "chat_history.json"


def _ensure_file() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_history() -> list[dict]:
    _ensure_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_history(entries: list[dict]) -> None:
    _ensure_file()
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def add_chat_entry(question: str, answer: str, sources: list[dict], question_type: str) -> dict:
    record = {
        "question": question.strip(),
        "answer": answer.strip(),
        "sources": sources,
        "type": question_type,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    entries = load_history()
    entries.insert(0, record)
    save_history(entries)
    return record


def get_recent_history(limit: int = 50) -> list[dict]:
    return load_history()[:limit]
