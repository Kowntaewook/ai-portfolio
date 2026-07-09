"""
실습 4: 유사도 검색 실험

목표:
- LLM 답변 생성 없이 검색 결과만 확인합니다.
- 질문과 k 값을 바꿔 검색 품질을 비교합니다.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def search(question: str, k: int = 2):
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("환경변수 GEMINI_API_KEY 또는 GOOGLE_API_KEY를 설정해야 합니다.")

    # TODO 1: 임베딩 객체를 만드세요.
    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )

    # TODO 2: 기존 ChromaDB를 불러오세요.
    db = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=emb)

    # TODO 3: similarity_search(question, k=k)를 실행하세요.
    hits = db.similarity_search(question, k=k)

    return hits


if __name__ == "__main__":
    question = "협업 경험이 드러나는 프로젝트는?"
    hits = search(question, k=2)

    print("질문:", question)
    for i, h in enumerate(hits, 1):
        print(f"\n[{i}위] {h.metadata.get('name', 'Unknown')}")
        print(h.page_content[:100], "...")

