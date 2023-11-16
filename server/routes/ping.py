import logging

from fastapi import APIRouter
from openai import APIConnectionError
from ..models.ping import Pong
from .upload import do_embed

ping_router = APIRouter()


@ping_router.get("/ping")
async def ping():
    """
    웹 서버와 모델 서버의 상태를 확인합니다.
    모델 서버가 꺼져 있으면 false를 반환합니다.
    """
    try:
        await do_embed("./server/static/sample.txt")
        pong = Pong(status=True)

    except APIConnectionError as e:
        logging.exception("%s : 모델 서버에 연결할 수 없습니다. 모델 서버 상태 또는 env 환경 변수를 확인해주세요. ", e)
        pong = Pong(status=False)
    return pong
