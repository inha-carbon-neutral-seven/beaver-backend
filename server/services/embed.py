"""
GET /embed
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""
import logging
import os

from llama_index import SimpleDirectoryReader, VectorStoreIndex
from openai import APIConnectionError

from .ping import check_server_status
from .storage import get_storage_path, load_table_filename


async def embed_file() -> bool:
    """
    저장소에 있는 파일을 모델 서버로 보내 임베딩 결과를 받아옴
    """
    storage_path = get_storage_path()
    raw_path = os.path.join(storage_path, "raw")
    embed_path = os.path.join(storage_path, "embed")
    table_filename = await load_table_filename()

    if table_filename is not None:
        logging.info("테이블 파일은 임베딩하지 않음")
        return True

    # 모델 서버가 불안정하면 임베딩을 진행하지 않음
    if await check_server_status() is False:
        return False

    documents = []

    try:
        documents = SimpleDirectoryReader(
            input_dir=raw_path,
            recursive=True,
        ).load_data(show_progress=True)
    except ValueError:
        logging.warning("저장소가 비어 있음")
        return False

    try:
        index = VectorStoreIndex.from_documents(documents, show_progress=True)

        if not os.path.exists(embed_path):
            os.makedirs(embed_path)
        index.storage_context.persist(persist_dir=embed_path)
    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        return False

    return True
