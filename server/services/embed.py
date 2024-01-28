"""
GET /embed
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import logging
import os

from openai import APIConnectionError

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


from .ping import check_server_status
from .storage import get_storage_path, load_table_filename
from .agents.recommendation_agent import lookup as recommendation_agent
from ..models.recommendation import RecommendationOutput
from .generate import generate_message


def embed_file() -> bool:
    """
    저장소에 있는 파일을 모델 서버로 보내 임베딩 결과(bool)를 받아옴
    """
    storage_path = get_storage_path()
    document_path = os.path.join(storage_path, "document")
    chroma_path = os.path.join(storage_path, "chroma")
    table_filename = load_table_filename()

    if table_filename is not None:
        logging.info("테이블 파일은 임베딩하지 않음")
        return True

    # 모델 서버가 불안정하면 임베딩을 진행하지 않음
    if check_server_status() is False:
        return False

    try:
        # 디렉토리를 읽어옵니다.
        loader = DirectoryLoader(document_path, show_progress=True)
        documents = loader.load()

    except ValueError:
        logging.warning("임베딩 실패: 저장소가 비어 있음")
        return False

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    # split documents
    splitted_documents = text_splitter.split_documents(documents)

    try:
        Chroma.from_documents(
            documents=splitted_documents,
            persist_directory=chroma_path,
            embedding=OpenAIEmbeddings(),
        )

    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        return False
    return True


def generate_recommendations() -> RecommendationOutput:
    """
    사용자가 물어볼 만한 적절한 질문을 파일 내용을 기반으로 생성합니다.
    """

    message = """
    주어진 문서에 대응하는 title, subtitle, description을 각각 작성해줘.
    """
    answer = generate_message(question_message=message)
    description = answer.message

    logging.info("description text: \n%s", description)

    result = recommendation_agent(description=description)

    return result
