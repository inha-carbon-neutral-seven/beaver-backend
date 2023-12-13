import logging
from llama_index import StorageContext, load_index_from_storage
from openai import APIConnectionError

from ..models.generate import Answer, Question

STORAGE_PATH = "./server/storage/user1"  # 저장 경로, 세션 별 관리를 위해 폴더 분리해둠

async def generate_service(question: Question) -> Answer:
    embed_path = STORAGE_PATH + "/embed"

    try:
        storage_context = StorageContext.from_defaults(persist_dir=embed_path)
        index = load_index_from_storage(storage_context)
    except FileNotFoundError:  # 사용자로부터 임베딩 파일을 받지 못했을 때 예외를 표출함
        logging.warning("저장소 내부가 비어 있음")
        return Answer(message="파일이 첨부되지 않았습니다.")

    try:
        if 1 == 0: # chat engine 사용 전에 자연스러운 프롬프트 처리가 필요함
            chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
            res = chat_engine.chat(message=question.message)
        # 자연스러운 응답을 생성하는 query engine으로 임시 설정
        query_engine = index.as_query_engine()
        res = query_engine.query(question.message)

        answer = Answer(message=res.response)
    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        return Answer(message="모델 서버 상태를 확인해주세요.")

    logging.info("생성한 응답: %s", answer.message)
    return answer
