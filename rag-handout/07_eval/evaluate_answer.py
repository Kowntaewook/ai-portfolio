"""
실습 7: RAG 평가 파이프라인
"""

import argparse
import json
import os
import re
import warnings
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

warnings.filterwarnings("ignore", category=FutureWarning)

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


EVAL_DIR = Path(__file__).resolve().parent
LESSON_DIR = EVAL_DIR.parent
DATASET_PATH = EVAL_DIR / "eval_dataset.json"
RESULTS_PATH = EVAL_DIR / "eval_results.jsonl"
CHROMA_DIR = LESSON_DIR / "chroma_db"


def load_dataset(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def preprocess_query(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip())


def build_queries(item: dict) -> list[str]:
    queries = []
    if question := item.get("question"):
        queries.append(question)

    for variant in item.get("query_variants", []) or []:
        if variant:
            queries.append(variant)

    seen = set()
    deduped = []
    for query in queries:
        normalized = preprocess_query(query)
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(normalized)

    return deduped


def create_llm_and_db():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(".env 파일에 GEMINI_API_KEY 또는 GOOGLE_API_KEY를 설정하세요.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2,
    )
    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )
    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=emb,
    )

    return llm, db


def retrieve_multi_query(db, queries: list[str], k: int) -> list:
    if not queries:
        return []

    unique_docs = []
    seen_names = set()
    for query in queries:
        docs = db.similarity_search(query, k=k)
        for doc in docs:
            if isinstance(doc.metadata, dict):
                name = doc.metadata.get("name")
            else:
                name = getattr(doc.metadata, "get", lambda _: None)("name")

            key = (name or str(doc)).strip()
            if key not in seen_names:
                seen_names.add(key)
                unique_docs.append(doc)

    return unique_docs


def format_docs(docs) -> str:
    if not docs:
        return "검색된 문서가 없습니다."

    formatted = []
    for doc in docs:
        title = "Unknown"
        if isinstance(doc.metadata, dict):
            title = doc.metadata.get("name", title)
        else:
            title = getattr(doc.metadata, "get", lambda _: None)("name") or title

        formatted.append(f"프로젝트명: {title}\n{doc.page_content}")

    return "\n\n".join(formatted)


def generate_answer(llm, question: str, docs) -> str:
    prompt = ChatPromptTemplate.from_template(
        """
너는 지원자의 포트폴리오를 소개하는 어시스턴트야.
아래 문서 내용만 근거로 답변해.
문서에 없는 내용은 "포트폴리오에 없는 정보입니다"라고 답해.
가능하면 답변에 근거가 된 프로젝트명을 포함해.

[문서]
{context}

[질문]
{question}
"""
    )

    context = format_docs(docs)
    prompt_value = prompt.invoke({"context": context, "question": question})
    response = llm.invoke(prompt_value)

    if hasattr(response, "message"):
        message = response.message
    elif hasattr(response, "messages") and response.messages:
        message = response.messages[0]
    else:
        return str(response)

    content = getattr(message, "content", None)
    if isinstance(content, list):
        if not content:
            return ""
        first = content[0]
        return first if isinstance(first, str) else json.dumps(first, ensure_ascii=False)

    return content if content is not None else str(message)


def evaluate_sources(found_sources: list[str], expected_sources: list[str]) -> dict:
    found_lower = [source.lower() for source in found_sources if source]
    missing = []
    for expected in expected_sources or []:
        if expected and expected.lower() not in found_lower:
            missing.append(expected)

    return {
        "expected_sources": expected_sources,
        "found_sources": found_sources,
        "missing_sources": missing,
        "source_pass": len(missing) == 0,
    }


def evaluate_answer(answer: str, expected_keywords: list[str], should_abstain: bool) -> dict:
    answer_text = (answer or "").strip()
    lower_answer = answer_text.lower()
    keywords = [kw for kw in expected_keywords or [] if kw]
    found_keywords = [kw for kw in keywords if kw.lower() in lower_answer]

    abstain_patterns = [
        "포트폴리오에 없는 정보입니다",
        "이 정보는 포트폴리오에 없습니다",
        "포트폴리오에 없습니다",
        "모르겠습니다",
        "알 수 없습니다",
        "정보가 없습니다",
    ]
    abstained = any(pattern in lower_answer for pattern in abstain_patterns)

    if should_abstain:
        if not keywords:
            passed = abstained
        else:
            passed = bool(found_keywords) and abstained
    else:
        passed = len(found_keywords) == len(keywords) and not abstained

    return {
        "answer": answer_text,
        "found_keywords": found_keywords,
        "expected_keywords": keywords,
        "abstained": abstained,
        "answer_pass": passed,
    }


def ask_human_judgement(item: dict, answer: str) -> bool:
    print("\n" + "-" * 80)
    print("[사람 평가 입력]")
    print("아래 기준과 모델 응답을 비교해서, 이 문항의 의도한 행동을 했으면 y를 입력합니다.")
    print("\n[질문]")
    print(item.get("question", ""))
    print("\n[정답/의도 기준]")
    print("- 난이도:", item.get("difficulty", "unknown"))
    print("- 의도:", item.get("intended_behavior", "(없음)"))
    print("- 기대 출처:", ", ".join(item.get("expected_sources", [])) or "(없음)")
    print("- 기대 키워드:", ", ".join(item.get("expected_keywords", [])) or "(없음)")
    print("- 보류 응답 필요:", "예" if item.get("should_abstain") else "아니오")
    print("\n[모델 응답]")
    print(answer)

    while True:
        choice = input("의도한 행동을 했나요? (y/n): ").strip().lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("y 또는 n을 입력해 주세요.")


def save_result(result: dict):
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--no-human", action="store_true")
    args = parser.parse_args()

    dataset = load_dataset(DATASET_PATH)
    llm, db = create_llm_and_db()

    for item in dataset:
        queries = build_queries(item)
        docs = retrieve_multi_query(db, queries, args.k)
        answer = generate_answer(llm, item.get("question", ""), docs)
        found_sources = [
            (doc.metadata.get("name") if isinstance(doc.metadata, dict) else getattr(doc.metadata, "get", lambda _: None)("name"))
            or "Unknown"
            for doc in docs
        ]

        source_eval = evaluate_sources(found_sources, item.get("expected_sources", []))
        answer_eval = evaluate_answer(answer, item.get("expected_keywords", []), item.get("should_abstain", False))
        human_pass = True if args.no_human else ask_human_judgement(item, answer)

        result = {
            "id": item.get("id"),
            "question": item.get("question"),
            "queries": queries,
            "found_sources": found_sources,
            **source_eval,
            **answer_eval,
            "human_pass": human_pass,
        }

        save_result(result)
        print("\n[결과]", json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
