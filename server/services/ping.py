"""
GET /ping 
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""
import logging
import os

import requests


async def check_server_status() -> bool:
    """
    모델 서버의 상태를 확인하는 함수
    """

    # 작업 시작
    api_base = os.getenv("OPENAI_API_BASE")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    organization_id = os.getenv("OPENAI_ORGANIZATION_ID")

    if api_base is None:
        api_base = "https://api.openai.com/v1"

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "OpenAI-Organization": organization_id,
    }
    url = api_base + "/models"

    try:
        response = requests.get(url, headers=headers, timeout=2)

        # HTTP 코드가 200이 아니면 예외를 일으킵니다.
        response.raise_for_status()
        return True

    except requests.exceptions.ConnectionError:
        logging.warning("모델 서버 연결 불가: 서버가 꺼진 것으로 추정")
        return False

    except requests.exceptions.Timeout:
        logging.warning("모델 서버 연결 불가: 모델 서버 불안정")
        return False

    except requests.exceptions.HTTPError as err:
        logging.warning("모델 서버 응답 오류: %s", err)
        return False
