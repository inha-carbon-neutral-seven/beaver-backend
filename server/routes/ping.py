from fastapi import APIRouter
from openai.error import APIConnectionError

from ..models.ping import Pong
from .upload import do_embed


ping_router = APIRouter()


@ping_router.get("/ping")
async def ping():
    """
    웹 서버와 모델 서버의 상태를 확인합니다.
    모델 서버가 꺼져 있으면 false를 return 합니다.
    """
    try:
        await do_embed("./server/static/sample.txt")
        pong = Pong(message=True)
    except APIConnectionError:
        pong = Pong(message=False)
    return pong
