"""
Vercel? ?? RAG ??
- ChromaDB / sentence-transformers / LangChain ??
- projects.json?? ?? ??? ??
- Gemini API? ?? ??
"""

import json
import os
import re
from typing import Any, Dict, List

from google import genai


def _tokens(text: str) -> List[str]:
    return [
        token
        for token in re.findall(r"[A-Za-z0-9?-?_+#.-]+", text.lower())
        if len(token) >= 2
    ]


class RAGEngine:
    def __init__(
        self,
        projects_json_path: str,
        gemini_api_key: str,
        top_k: int = 3,
        **kwargs: Any,
    ):
        self.projects_json_path = projects_json_path
        self.gemini_api_key = gemini_api_key
        self.top_k = top_k
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = genai.Client(api_key=gemini_api_key)
        self.documents = self._load_projects()

    def _load_projects(self) -> List[Dict[str, Any]]:
        with open(self.projects_json_path, "r", encoding="utf-8-sig") as f:
            projects = json.load(f)

        documents = []
        for idx, project in enumerate(projects):
            title = project.get("title", "N/A")
            description = project.get("description", "")
            tags = ", ".join(project.get("tags", []))
            content = project.get("content", "")

            text = f"""????: {title}
??: {description}
??: {tags}

?? ??:
{content}
"""

            documents.append(
                {
                    "id": idx,
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "content": content,
                    "text": text,
                }
            )

        print(f"? {len(documents)}? ???? ?? ??")
        return documents

    def build_vectorstore(self) -> None:
        print("? Vercel ?? ??: ??DB ??")

    def build_qa_chain(self) -> None:
        print("? Vercel ?? ??: QA Chain ??")

    @classmethod
    def from_existing_db(
        cls,
        projects_json_path: str,
        gemini_api_key: str,
        **kwargs: Any,
    ):
        return cls(
            projects_json_path=projects_json_path,
            gemini_api_key=gemini_api_key,
            **kwargs,
        )

    def _search(self, question: str) -> List[Dict[str, Any]]:
        q_tokens = set(_tokens(question))
        scored = []

        for doc in self.documents:
            text = doc["text"].lower()
            d_tokens = set(_tokens(text))

            score = len(q_tokens & d_tokens)

            for token in q_tokens:
                if token in doc["title"].lower():
                    score += 3
                elif token in doc["tags"].lower():
                    score += 2
                elif token in text:
                    score += 0.5

            scored.append((score, doc))

        scored.sort(key=lambda item: item[0], reverse=True)

        selected = [doc for score, doc in scored if score > 0][: self.top_k]
        if not selected:
            selected = self.documents[: self.top_k]

        return selected

    def query(self, question: str) -> Dict[str, Any]:
        selected_docs = self._search(question)

        context = "\n\n---\n\n".join(doc["text"] for doc in selected_docs)

        prompt = f"""?? ???? AI ????? ?? ????.
?? ???? ??? ??? ????.
??? ??? ???? ??, ????? ????? ???? ???? ???.
??? ???? ????? ????.

[???? ??]
{context}

[??]
{question}

[??]
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        answer = getattr(response, "text", None) or "??? ???? ?????."

        sources = [
            {
                "title": doc["title"],
                "content_preview": doc["text"][:120] + "...",
            }
            for doc in selected_docs
        ]

        return {
            "answer": answer,
            "sources": sources,
        }


def build_rag_engine(
    projects_json_path: str,
    gemini_api_key: str,
    rebuild: bool = False,
    **kwargs: Any,
) -> RAGEngine:
    print("??? Vercel ?? RAG ?? ???")
    engine = RAGEngine(
        projects_json_path=projects_json_path,
        gemini_api_key=gemini_api_key,
        **kwargs,
    )
    engine.build_vectorstore()
    engine.build_qa_chain()
    return engine
