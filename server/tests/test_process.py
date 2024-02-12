import pytest

from fastapi.testclient import TestClient

from ..main import app
from ..models.process import ProcessOutput
from ..models.recap import RecapOutput
from ..services import storage as storage_services


@pytest.fixture(autouse=True)
def clear_after_test():
    storage_services.clear_storage()


# 테스트 함수는 "test_~" 로 이름을 지어야 합니다
with TestClient(app) as client:

    def test_process_without_upload():
        for process_type in ["recap", "chart", "recommendation"]:
            response = client.post("/process", json={"type": process_type})

            assert response.status_code == 200

            process_output = ProcessOutput(**response.json())
            assert process_output.status is False
            assert process_output.output is None

    def test_process_recap_with_document():
        _upload_sample("document")

        response = client.post("/process", json={"type": "recap"})

        assert response.status_code == 200

        process_output = ProcessOutput(**response.json())
        assert process_output.status is True
        assert isinstance(process_output.output, RecapOutput)

    def test_process_recap_with_table():
        _upload_sample("table")

        response = client.post("/process", json={"type": "recap"})

        assert response.status_code == 200

        process_output = ProcessOutput(**response.json())
        assert process_output.status is True
        assert isinstance(process_output.output, RecapOutput)

    def test_process_recommendation_with_document():
        _upload_sample("document")

        response = client.post("/process", json={"type": "recommendation"})

        assert response.status_code == 200

        process_output = ProcessOutput(**response.json())
        assert process_output.status is True
        assert isinstance(process_output.output, list)

    def test_process_recommendation_with_table():
        _upload_sample("table")

        # /process 엔드포인트 호출
        response = client.post("/process", json={"type": "recommendation"})

        # 응답 상태 코드와 내용 확인
        assert response.status_code == 200

        process_output = ProcessOutput(**response.json())

        assert process_output.status is True
        assert isinstance(process_output.output, list)

    def test_process_chart_with_document():
        _upload_sample("document")

        response = client.post("/process", json={"type": "chart"})

        # 응답 상태 코드와 내용 확인
        assert response.status_code == 200

        process_output = ProcessOutput(**response.json())

        assert process_output.status is True
        assert process_output.output is None

    def test_process_chart_with_table():
        _upload_sample("table")

        # response = client.post("/process", json={"type": "chart"})

        assert True

    # logics ###

    def _upload_sample(file_type: str = "document"):
        document_file_path = "./server/tests/static/sample_document.txt"
        table_file_path = "./server/tests/static/sample_table.csv"

        if file_type == "document":
            file_path = document_file_path
        else:
            file_path = table_file_path

        with open(file_path, "rb") as f:
            client.post("/upload", data={"description": "Test"}, files={"file": f})
