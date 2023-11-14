from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

"""
테스트 케이스 작성 시 함수 이름을 test_ 로 지어야 합니다.
"""


def test_모델_서버_상태_확인():
    response = client.get("/ping")
    assert response.status_code == 200
    assert "status" in response.json()
