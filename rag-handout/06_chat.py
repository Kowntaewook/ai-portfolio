"""
실습 6: 터미널 챗봇

목표:
- 사용자가 질문을 계속 입력할 수 있는 대화 루프를 만듭니다.
- exit 또는 quit 입력 시 종료합니다.
"""

import importlib.util
from pathlib import Path


def _load_step05():
    path = Path(__file__).resolve().parent / "05_qna_chain.py"
    spec = importlib.util.spec_from_file_location("step05_qna_chain", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("05_qna_chain.py를 불러올 수 없습니다.")
    spec.loader.exec_module(module)
    return module


chain = _load_step05().chain


print("포트폴리오 챗봇입니다. exit 입력 시 종료.")

while True:
    # TODO 1: input()으로 질문을 받으세요.
    q = input("질문을 입력하세요: ").strip()

    # TODO 2: exit 또는 quit이면 반복문을 종료하세요.
    if q.lower() in {"exit", "quit"}:
        print("챗봇을 종료합니다.")
        break

    # TODO 3: chain.invoke(q)를 실행하고 출력하세요.
    try:
        answer = chain.invoke(q)
    except Exception as e:
        print("답변 생성 중 오류가 발생했습니다:", e)
        continue

    print(answer)
