import logging
import os
import requests

from dotenv import load_dotenv


async def ping_service() -> bool:
    load_dotenv()
    base_url = os.getenv("OPENAI_BASE_URL")

    try:  # GET /v1/models 에 요청을 보내 모델 서버 상태를 확인함
        requests.get(base_url + "/models", timeout=2)

    except requests.exceptions.ConnectionError:  # 서버가 꺼져있을 때
        logging.warning("모델 서버 연결 불가: 서버가 꺼진 것으로 추정")
        return False

    except requests.exceptions.Timeout:  # 타임아웃
        logging.warning("모델 서버 연결 불가: 모델 서버 불안정")
        return False

    return True
