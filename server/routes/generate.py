from fastapi import APIRouter, Request

from ..services.session import set_user_id
from ..services.generate import generate_message
from ..models.generate import Answer, Question

generate_router = APIRouter()


@generate_router.post("/generate")
async def generate(request: Request, question: Question) -> Answer:
    """
    메시지를 생성합니다.
    """

    set_user_id(request=request)
    answer = await generate_message(question)
    return answer
