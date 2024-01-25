from fastapi import APIRouter, Request

from ..models.generate import Answer, Question
from ..services.generate import generate_message
from ..services.session import set_user_id


generate_router = APIRouter()


@generate_router.post("/generate")
async def generate(request: Request, question: Question) -> Answer:
    """
    메시지를 생성합니다.
    """

    set_user_id(request=request)
    answer = await generate_message(question.message)
    return answer
