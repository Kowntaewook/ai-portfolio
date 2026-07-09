"""
FastAPI 챗봇 API 서버

엔드포인트:
- POST /chat: 질문을 받아 RAG 답변 반환
- GET /health: 서버 상태 확인
"""

import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from .rag_core import build_rag_engine
    from .guestbook import add_guestbook_entry, get_recent_guestbook
    from .project_stats import get_all_stats, get_stats, increment_view, toggle_like, get_popular_projects
    from .feedback import add_feedback, get_feedback_stats, get_recent_feedback
    from .chat_history import add_chat_entry, get_recent_history
    from .router import QuestionRouter, QuestionType
    from .github_tool import get_repository_info
except ImportError:
    from rag_core import build_rag_engine
    from guestbook import add_guestbook_entry, get_recent_guestbook
    from project_stats import get_all_stats, get_stats, increment_view, toggle_like, get_popular_projects
    from feedback import add_feedback, get_feedback_stats, get_recent_feedback
    from chat_history import add_chat_entry, get_recent_history
    from router import QuestionRouter, QuestionType
    from github_tool import get_repository_info

# 환경변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="AI Portfolio RAG API",
    description="프로젝트 포트폴리오 질의응답 API",
    version="1.0.0"
)

# CORS 설정 (웹에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG 엔진 전역 변수
rag_engine = None
question_router = QuestionRouter()


# 요청/응답 모델 정의
class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list
    question_type: str


class GuestbookRequest(BaseModel):
    name: str
    message: str


class StatsResponse(BaseModel):
    views: int
    likes: int
    liked: bool


class LikeRequest(BaseModel):
    user_id: str = Field(..., description="익명 사용자 ID")


class LikeResponse(BaseModel):
    liked: bool
    views: int
    likes: int


class FeedbackRequest(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str


class FeedbackResponse(BaseModel):
    name: str
    rating: int
    comment: str
    created_at: str


class GitHubInfoResponse(BaseModel):
    full_name: str
    description: Optional[str]
    html_url: str
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    watchers_count: int
    language: Optional[str]
    license: Optional[str]
    updated_at: Optional[str]


class AdminSummaryResponse(BaseModel):
    total_guestbook: int
    total_feedback: int
    average_feedback_rating: float
    total_chats: int
    popular_projects: list[dict]


@app.on_event("startup")
async def startup_event():
    """
    서버 시작 시 RAG 엔진 초기화
    """
    global rag_engine

    # API 키 확인
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다.")

    # projects.json 경로
    projects_json = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "projects.json"
    )

    print("🚀 RAG 엔진 초기화 중...")

    # RAG 엔진 빌드
    persist_directory = os.getenv("CHROMA_DIR", "/tmp/chroma_db" if os.getenv("VERCEL") else "./chroma_db")
    rag_engine = build_rag_engine(
        projects_json_path=projects_json,
        gemini_api_key=gemini_api_key,
        rebuild=True,  # 수정: 벡터 DB 재구축 (프롬프트/문서 변경 적용)
        top_k=2,
        chunk_size=1000,
        chunk_overlap=0,
        persist_directory=persist_directory
    )

    print("✅ RAG 엔진 준비 완료!")


@app.get("/")
async def root():
    """
    API 루트 - 간단한 정보 반환
    """
    return {
        "message": "AI Portfolio RAG API",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - 챗봇 질의응답",
            "/health": "GET - 서버 상태 확인",
            "/guestbook": "GET/POST - 방명록 조회/등록",
            "/stats": "GET - 프로젝트 통계",
            "/stats/{project_id}/view": "POST - 프로젝트 조회수 증가",
            "/stats/{project_id}/like": "POST - 프로젝트 좋아요 토글",
            "/recommendations": "GET - 인기 프로젝트 추천",
            "/feedback": "GET/POST - 피드백 조회/등록",
            "/chat/history": "GET - 최근 챗 히스토리",
            "/github": "GET - GitHub 저장소 정보 조회",
            "/admin/summary": "GET - 어드민 통계 요약"
        }
    }


@app.get("/health")
async def health_check():
    """
    서버 상태 확인
    """
    if rag_engine is None:
        raise HTTPException(status_code=503, detail="RAG 엔진이 초기화되지 않았습니다.")

    return {
        "status": "healthy",
        "rag_engine": "ready"
    }


def _normalize_question(question: str) -> str:
    return question.strip()


def _build_chat_response(question: str, result: dict, question_type: str) -> ChatResponse:
    add_chat_entry(
        question=question,
        answer=result['answer'],
        sources=result['sources'],
        question_type=question_type
    )
    return ChatResponse(
        answer=result['answer'],
        sources=result['sources'],
        question_type=question_type
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    챗봇 질의응답

    Args:
        request: 질문 요청

    Returns:
        답변 및 출처
    """
    if rag_engine is None:
        raise HTTPException(status_code=503, detail="RAG 엔진이 초기화되지 않았습니다.")

    question = _normalize_question(request.question)
    if not question:
        raise HTTPException(status_code=400, detail="질문이 비어있습니다.")

    question_type = question_router.classify(question).value
    if question_type == QuestionType.UNKNOWN.value:
        raise HTTPException(status_code=400, detail="지원하지 않는 질문입니다.")

    try:
        result = rag_engine.query(question)
        lower = question.lower()
        if any(keyword in lower for keyword in ["github", "repo", "repository"]):
            try:
                repo_info = get_repository_info()
                result['answer'] += (
                    "\n\n[GitHub 정보]\n"
                    f"{repo_info.get('full_name')} - {repo_info.get('description')}\n"
                    f"stars: {repo_info.get('stargazers_count')}, forks: {repo_info.get('forks_count')}\n"
                    f"url: {repo_info.get('html_url')}"
                )
                result['sources'].append({
                    'title': 'GitHub Repository',
                    'content_preview': repo_info.get('html_url')
                })
            except Exception:
                pass

        return _build_chat_response(question, result, question_type)

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"답변 생성 중 오류: {str(e)}")


@app.get("/guestbook")
async def list_guestbook(limit: int = Query(20, ge=1, le=100)) -> list[dict]:
    return get_recent_guestbook(limit)


@app.post("/guestbook")
async def post_guestbook(entry: GuestbookRequest) -> dict:
    try:
        return add_guestbook_entry(entry.name, entry.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/stats")
async def stats() -> dict:
    return get_all_stats()


@app.get("/stats/{project_id}", response_model=StatsResponse)
async def stats_for_project(project_id: str) -> StatsResponse:
    return StatsResponse(**get_stats(project_id))


@app.post("/stats/{project_id}/view")
async def project_view(project_id: str) -> dict:
    return increment_view(project_id)


@app.post("/stats/{project_id}/like", response_model=LikeResponse)
async def project_like(project_id: str, request: LikeRequest) -> LikeResponse:
    try:
        return LikeResponse(**toggle_like(project_id, request.user_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/recommendations")
async def recommendations(limit: int = Query(5, ge=1, le=20)) -> list[dict]:
    return get_popular_projects(limit)


@app.get("/feedback")
async def list_feedback(limit: int = Query(20, ge=1, le=100)) -> dict:
    return {
        "stats": get_feedback_stats(),
        "items": get_recent_feedback(limit)
    }


@app.post("/feedback")
async def post_feedback(request: FeedbackRequest) -> FeedbackResponse:
    try:
        feedback = add_feedback(request.name, request.rating, request.comment)
        return FeedbackResponse(**feedback)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/chat/history")
async def chat_history(limit: int = Query(50, ge=1, le=200)) -> list[dict]:
    return get_recent_history(limit)


@app.get("/github", response_model=GitHubInfoResponse)
async def github_info(repo: Optional[str] = None) -> GitHubInfoResponse:
    try:
        return GitHubInfoResponse(**get_repository_info(repo))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/summary", response_model=AdminSummaryResponse)
async def admin_summary() -> AdminSummaryResponse:
    guestbook_items = get_recent_guestbook(1000)
    feedback_items = get_recent_feedback(1000)
    chat_items = get_recent_history(1000)
    return AdminSummaryResponse(
        total_guestbook=len(guestbook_items),
        total_feedback=len(feedback_items),
        average_feedback_rating=get_feedback_stats().get("average_rating", 0.0),
        total_chats=len(chat_items),
        popular_projects=get_popular_projects(5)
    )


if __name__ == "__main__":
    import uvicorn

    # 개발 서버 실행
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 코드 변경 시 자동 재시작
    )
