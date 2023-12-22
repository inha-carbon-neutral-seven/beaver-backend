import os
import logging
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from openai import APIConnectionError

from .ping_service import check_server_status

STORAGE_PATH = "./server/storage/user1"  # 저장 경로, 세션 별 관리를 위해 폴더 분리해둠


async def embed_file() -> bool:
    """
    저장소에 있는 파일을 모델 서버로 보내 임베딩 결과를 받아옴
    """

    ## 23/12/22 !! 테이블 데이터 임베딩 비활성화 !!
    if 1 == 1:
        return True

    # 모델 서버가 불안정하면 임베딩을 진행하지 않음
    if await check_server_status() is False:
        return False

    raw_path = STORAGE_PATH + "/raw"
    embed_path = STORAGE_PATH + "/embed"
    docs = []

    try:
        docs = SimpleDirectoryReader(input_dir=raw_path, recursive=True).load_data()
    except ValueError:
        logging.warning("저장소가 비어 있음")
        return False

    try:
        index = VectorStoreIndex.from_documents(docs)
        if not os.path.exists(embed_path):
            os.makedirs(embed_path)
        index.storage_context.persist(persist_dir=embed_path)
    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        return False

    return True
