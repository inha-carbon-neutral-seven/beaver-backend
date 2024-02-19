from fastapi import APIRouter

from ..models.generate import Answer, Question
from ..services.debug import run_generate as generate_debug
from ..services.generate import generate_message


generate_router = APIRouter()


@generate_router.post("/generate")
async def generate(question: Question) -> Answer:
    """
    메시지를 생성합니다.
    """

    answer = generate_message(question.message)
    return answer


@generate_router.post("/debug/generate")
async def debug(question: Question) -> Answer:
    """
    메시지를 생성합니다.
    """

    answer = generate_debug(question.message)
    return answer
