import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from ..main import app


# 테스트 함수는 "test_~" 로 이름을 지어야 합니다
with TestClient(app) as client:

    def test_env():
        load_dotenv()

        assert "OPENAI_API_KEY" in os.environ, "OPENAI_API_KEY 환경 변수가 필요합니다."
