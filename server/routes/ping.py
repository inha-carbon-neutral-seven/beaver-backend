import logging
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter

from ..models.ping import Pong

ping_router = APIRouter()


@ping_router.get("/ping")
async def ping():
    load_dotenv()
    base_url = os.getenv("OPENAI_BASE_URL")
    try:
        # GET /v1/models 에 요청을 보내 모델 서버 상태를 확인함
        requests.get(base_url + "/models", timeout=2)
    except requests.exceptions.Timeout:
        logging.warning("모델 서버에 연결할 수 없음")
        return Pong(status=False)

    return Pong(status=True)
