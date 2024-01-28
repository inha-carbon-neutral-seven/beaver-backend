"""
GET /embed
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import logging

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .ping import check_server_status
from .storage import get_document_path, get_chroma_path
from .agents.recommendation_agent import lookup as recommendation_agent
from ..models.recommendation import RecommendationOutput
from .generate import generate_message


def embed_document() -> bool:
    """
    저장소에 있는 파일을 모델 서버로 보내 임베딩 결과를 받아옵니다.
    """

    # 모델 서버가 불안정하면 임베딩을 진행하지 않음
    if check_server_status() is False:
        return False

    # 문서 파일 임베딩
    document_path = get_document_path()
    chroma_path = get_chroma_path()

    try:
        # 디렉토리를 읽어옵니다. [UnstructuredFileLoader]
        loader = DirectoryLoader(document_path, show_progress=True)
        documents = loader.load()

    except ValueError:
        logging.warning("문서 임베딩 오류: 저장소를 읽을 수 없음")
        return False

    # split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        add_start_index=True,
    )
    splitted_documents = text_splitter.split_documents(documents)

    try:
        # persist documents
        Chroma.from_documents(
            documents=splitted_documents,
            persist_directory=chroma_path,
            embedding=OpenAIEmbeddings(),
        )

    except ValueError:
        logging.warning("문서 임베딩 오류: 모델 서버에 연결할 수 없음")
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

    result = recommendation_agent(description=description)

    return result
