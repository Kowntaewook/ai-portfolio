"""
실습 5: QnA 체인 완성

목표:
- retriever, prompt, llm을 LCEL 파이프(|)로 연결합니다.
- 검색된 문서만 근거로 답변하게 만듭니다.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


def format_docs(docs):
    # TODO: Document 리스트를 하나의 문자열로 합치세요.
    if not docs:
        return "검색된 문서가 없습니다."

    formatted = []
    for doc in docs:
        title = doc.metadata.get("name", "Unknown")
        formatted.append(f"프로젝트명: {title}\n{doc.page_content}")
    return "\n\n".join(formatted)


def create_chain():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(".env 파일에 GEMINI_API_KEY 또는 GOOGLE_API_KEY를 설정하세요.")

    # TODO 1: llm, emb, db, retriever를 준비하세요.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2,
    )
    emb = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )
    db = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=emb)
    retriever = db.as_retriever(search_kwargs={"k": 2})

    # TODO 2: ChatPromptTemplate.from_template(...)로 프롬프트를 만드세요.
    prompt = ChatPromptTemplate.from_template(
        """당신은 지원자의 포트폴리오를 분석하고 설명하는 전문 어시스턴트입니다.

아래 포트폴리오 정보만을 사용하여 사용자의 질문에 직접적이고 명확하게 답변해주세요.

## 포트폴리오 정보
{context}

## 답변 가이드
- 제공된 포트폴리오 정보에 없는 내용은 "이 정보는 포트폴리오에 없습니다."라고 명시하세요.
- 답변할 때는 관련 프로젝트명, 기간, 역할을 함께 언급하면 더 도움이 됩니다.
- 요청자의 궁금한 점에 직접 답하되, 과장하지 마세요.
- 마크다운 포맷을 사용하여 읽기 쉽게 정렬하세요.

## 사용자 질문
{question}

## 답변"""
    )

    # TODO 3: LCEL 체인을 조립하세요.
    chain = RunnableLambda(lambda question: {
        "context": format_docs(retriever.invoke(question)),
        "question": question,
    }) | prompt | llm

    return chain


chain = create_chain()


if __name__ == "__main__":
    print(chain.invoke("가장 도전적이었던 프로젝트는?"))

