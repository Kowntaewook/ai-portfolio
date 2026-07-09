"""
실습 3: 벡터 인덱스 구축

목표:
- chunk를 Gemini 임베딩으로 변환합니다.
- ChromaDB에 저장합니다.
"""

import importlib.util
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def _load_step02():
    path = Path(__file__).resolve().parent / "02_split_docs.py"
    spec = importlib.util.spec_from_file_location("step02_split_docs", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("02_split_docs.py를 불러올 수 없습니다.")
    spec.loader.exec_module(module)
    return module


def build_index():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("환경변수 GEMINI_API_KEY 또는 GOOGLE_API_KEY를 설정해야 합니다.")

    # TODO 1: split_documents()로 chunks를 가져오세요.
    chunks = _load_step02().split_documents()[1]

    # TODO 2: GoogleGenerativeAIEmbeddings를 만드세요.
    # 힌트: model="models/gemini-embedding-001"
    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )

    # TODO 3: Chroma.from_documents(...)로 DB를 만들고 CHROMA_DIR에 저장하세요.
    db = Chroma.from_documents(
        documents=chunks,
        embedding=emb,
        persist_directory=str(CHROMA_DIR),
    )

    return db, len(chunks)


if __name__ == "__main__":
    db, count = build_index()
    print("저장된 조각:", count)

