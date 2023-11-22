import logging

from llama_index import StorageContext, load_index_from_storage
from openai import APIConnectionError

from fastapi import APIRouter, HTTPException

from ..models.generate import Answer, Question


generate_router = APIRouter()


STORAGE_PATH = "./server/storage/user1"  # 저장 경로, 세션 별 관리를 위해 폴더 분리해둠


@generate_router.post("/generate")
async def generate_message(question: Question):
    """
    [v] 모델 서버에 대답을 요청하여 클라이언트에게 전달합니다.
    [ ] 또한, 대화 기록을 서버에 저장합니다.
    """

    embed_path = STORAGE_PATH + "/embed"

    try:
        storage_context = StorageContext.from_defaults(persist_dir=embed_path)
        index = load_index_from_storage(storage_context)
    except FileNotFoundError:
        logging.warning("저장소 내부가 비어 있음")
        HTTPException(status_code=404, detail="저장소가 비어 있음")

    try:
        if False:  # 자연스러운 응답을 생성하는 Completion 모델로 임시 설정
            chat_engine = index.as_chat_engine(
                chat_mode="condense_question", verbose=True
            )
            res = chat_engine.chat(message=question.message)
        query_engine = index.as_query_engine()
        res = query_engine.query(question.message)

        answer = Answer(message=res.response)
    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        HTTPException(status_code=502, detail="모델 서버에 연결할 수 없음")

    logging.info("생성한 응답: %s", answer.message)
    return answer
