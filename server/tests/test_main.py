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


def test_대답_생성_확인():
    data = {"message": "대한민국의 수도는 어디야?"}
    response = client.post("/generate", json=data)
    assert response.status_code == 200
    assert "message" in response.json()  # env 리팩터링 전까지는 모델 서버 확인해달라는 응답만 돌아와요
