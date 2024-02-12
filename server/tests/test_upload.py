import os

from fastapi.testclient import TestClient

from ..main import app


# 테스트 함수는 "test_~" 로 이름을 지어야 합니다
with TestClient(app) as client:

    def test_upload():
        file_path = "./server/tests/static/sample_document.txt"

        assert os.path.exists(file_path)

        with open(file_path, "rb") as f:
            response = client.post("/upload", data={"description": "Test"}, files={"file": f})

        # 응답 상태 코드와 내용 확인
        assert response.status_code == 200
        assert response.json() == {"filename": "sample_document.txt", "description": "Test"}
