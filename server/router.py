"""
질문 라우팅 시스템
"""

from enum import Enum


class QuestionType(Enum):
    PROJECT = "project"
    GENERAL = "general"
    UNKNOWN = "unknown"


class QuestionRouter:
    """질문을 분류하는 라우터"""

    def __init__(self):
        self.project_keywords = [
            "프로젝트", "project", "경험", "기술", "개발", "역할", "구현", "서비스", "시스템",
            "포트폴리오", "팀", "협업", "백엔드", "프론트", "웹", "AI", "RAG", "챗봇", "데이터"
        ]
        self.general_patterns = [
            "안녕", "hello", "hi", "감사", "thank", "잘지내", "좋아", "어때", "휴가", "날씨",
            "이름", "무엇", "뭐", "어떻게", "왜", "기분"
        ]
        self.unknown_keywords = [
            "연봉", "salary", "나이", "age", "전공", "학력", "학교", "주소", "거주지", "전화번호",
            "지원 동기", "가족", "결혼", "종교", "정치", "비밀번호"
        ]

    def classify(self, question: str) -> QuestionType:
        question_lower = (question or "").strip().lower()
        if not question_lower:
            return QuestionType.UNKNOWN

        if any(keyword in question_lower for keyword in self.unknown_keywords):
            return QuestionType.UNKNOWN
        if any(pattern in question_lower for pattern in self.general_patterns):
            return QuestionType.GENERAL
        if any(keyword in question_lower for keyword in self.project_keywords):
            return QuestionType.PROJECT

        # 애매할 때는 기본적으로 포트폴리오 관련 질문으로 처리
        return QuestionType.PROJECT
