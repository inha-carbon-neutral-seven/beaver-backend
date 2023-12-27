import logging
import os
import requests

from dotenv import load_dotenv


async def check_server_status() -> bool:
    """
    모델 서버의 상태를 확인하는 함수
    """
    load_dotenv()
    base_url = os.getenv("OPENAI_BASE_URL")

    try:
        # 모델 서버에 GET /v1/models 에 요청을 보냅니다.
        requests.get(base_url + "/models", timeout=2)

    except requests.exceptions.ConnectionError:  # 서버가 꺼져있을 때
        logging.warning("모델 서버 연결 불가: 서버가 꺼진 것으로 추정")
        return False

    except requests.exceptions.Timeout:  # 타임아웃
        logging.warning("모델 서버 연결 불가: 모델 서버 불안정")
        return False

    return True
