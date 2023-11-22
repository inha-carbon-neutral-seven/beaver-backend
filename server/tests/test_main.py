from fastapi.testclient import TestClient

from ..main import app


# 테스트 함수는 "test_~" 로 이름을 지어야 합니다
with TestClient(app) as client:

    def test_모델_서버_상태_확인():
        response = client.get("/ping")
        assert response.status_code == 200

    def test_대답_생성_확인():
        data = {"message": "대한민국의 수도는 어디야?"}
        response = client.post("/generate", json=data)
        assert response.status_code == 200
