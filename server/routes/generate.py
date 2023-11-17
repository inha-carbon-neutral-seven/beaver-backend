import logging

from fastapi import APIRouter
from llama_index import StorageContext, load_index_from_storage

from openai import APIConnectionError

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
        return Answer(message="파일이 첨부되지 않았습니다.")

    try:
        chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
        res = chat_engine.chat(message=question.message)
        answer = Answer(message=res.response)
    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        return Answer(message="모델 서버 상태를 확인해주세요.")

    logging.info("생성한 응답: %s", answer.message)
    return answer
