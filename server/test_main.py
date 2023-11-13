from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


def 모델_서버_상태_확인():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
