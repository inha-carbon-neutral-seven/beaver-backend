import pytest

from fastapi.testclient import TestClient

from ..main import app
from ..models.generate import Answer, AnswerType
from ..models.process import ProcessInput, ProcessType
from ..services import storage as storage_services
from .test_upload import test_upload_document, test_upload_table


@pytest.fixture(autouse=True)
def setup():
    storage_services.clear_storage()


# 테스트 함수는 "test_~" 로 이름을 지어야 합니다
with TestClient(app) as client:

    def test_generate_without_upload():
        # without upload
        # without embed

        response = client.post("/generate", json={"message": "파일 내용을 설명해주세요."})

        # 응답 상태 코드와 내용 확인
        assert response.status_code == 200

        answer = Answer(**response.json())

        assert answer.type == AnswerType.TEXT
        assert answer.chart is None

    def test_generate_without_embed():
        _upload_sample()
        # without embed

        response = client.post("/generate", json={"message": "파일 내용을 설명해주세요."})

        assert response.status_code == 200

        answer = Answer(**response.json())

        assert answer.type == AnswerType.TEXT
        assert answer.chart is None

    def test_generate_with_document():
        _upload_sample()
        _embed()

        response = client.post("/generate", json={"message": "파일 내용을 설명해주세요."})

        assert response.status_code == 200

        answer = Answer(**response.json())

        assert answer.type == AnswerType.TEXT
        assert answer.chart is None

    # logics ###

    def _upload_sample(file_type: str = "document"):
        if file_type == "document":
            test_upload_document()
        else:
            test_upload_table()

    def _embed():
        process_input = ProcessInput(type=ProcessType.EMBED)
        client.post("/process", json=process_input.model_dump())
