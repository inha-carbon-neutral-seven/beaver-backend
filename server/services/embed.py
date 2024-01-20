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
from .agents.recommendation_agent import lookup as recommendation_agent
from ..models.recommendation import RecommendationOutput


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


async def generate_recommendations() -> RecommendationOutput:
    """
    사용자가 물어볼 만한 적절한 질문을 파일 내용을 기반으로 생성합니다.
    """

    # TODO: 업로드 파일에 대한 간략한 설명을 description으로 생성해낼 것

    description = """
    The data is a pandas dataframe with 112,191 entries 
    and 18 columns representing various attributes of items in a store.
    """

    result = recommendation_agent(description=description)

    return result
