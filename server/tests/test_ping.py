from fastapi.testclient import TestClient

from ..main import app


# 테스트 함수는 "test_~" 로 이름을 지어야 합니다
with TestClient(app) as client:

    def test_ping():
        response = client.get("/ping")
        assert response.status_code == 200
        assert "status" in response.json()
