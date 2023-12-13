import os
import logging
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from openai import APIConnectionError

from .ping_service import ping_service

STORAGE_PATH = "./server/storage/user1"  # 저장 경로, 세션 별 관리를 위해 폴더 분리해둠

async def embed_service() -> bool:
    # 먼저 모델 서버 상태가 유효한지 확인함
    status = await ping_service()
    if status is False:
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
