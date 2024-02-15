import csv
import os

from fastapi.testclient import TestClient

from ..main import app


# 테스트 함수는 "test_~" 로 이름을 지어야 합니다
with TestClient(app) as client:

    def test_upload_document():
        file_content = b"sample text"
        file_name = "sample.txt"

        # 임시 파일을 생성하고 내용을 작성
        with open(file_name, "wb") as f:
            f.write(file_content)

        # 임시 파일을 열고 바이너리 모드로 읽어서 전송
        with open(file_name, "rb") as f:
            response = client.post("/upload", data={"description": "Test"}, files={"file": f})

        # 응답 상태 코드와 내용 확인
        assert response.status_code == 200
        assert response.json() == {"filename": file_name, "description": "Test"}

        # 테스트가 끝난 후 파일 삭제
        os.remove(file_name)

    def test_upload_table():
        # 샘플 CSV 데이터
        csv_data = [
            {"name": "John", "age": 30},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 35},
        ]

        # CSV 파일 경로
        file_name = "sample.csv"

        # CSV 파일 작성
        with open(file_name, "w", encoding="utf-8") as csvfile:
            fieldnames = ["name", "age"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in csv_data:
                writer.writerow(row)

        # CSV 파일을 열고 바이너리 모드로 읽어서 전송
        with open(file_name, "rb") as f:
            response = client.post("/upload", data={"description": "Test"}, files={"file": f})

        # 응답 상태 코드와 내용 확인
        assert response.status_code == 200
        assert response.json() == {"filename": file_name, "description": "Test"}

        # 테스트가 끝난 후 파일 삭제
        os.remove(file_name)
