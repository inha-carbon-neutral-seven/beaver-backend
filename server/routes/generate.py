from fastapi import APIRouter
from ..services.generate import generate_message
from ..models.generate import Answer, Question

generate_router = APIRouter()


@generate_router.post("/generate")
async def generate(question: Question) -> Answer:
    """
    메시지를 생성합니다.
    """
    answer = await generate_message(question)
    return answer
