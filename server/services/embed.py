"""
GET /embed
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""
import logging
import os

#from llama_index import SimpleDirectoryReader, VectorStoreIndex
from openai import APIConnectionError

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from .ping import check_server_status
from .storage import get_storage_path, load_table_filename
from .agents.recommendation_agent import lookup as recommendation_agent
from ..models.recommendation import RecommendationOutput
from .generate import generate_message


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
        """
        디렉토리 읽어옵니다.
        """
        loader = DirectoryLoader(raw_path, glob="*.txt", loader_cls=TextLoader, show_progress=True)
        documents = loader.load()

        # documents = SimpleDirectoryReader(
        #     input_dir=raw_path,
        #     recursive=True,
        # ).load_data(show_progress=True)
    except ValueError:
        logging.warning("저장소가 비어 있음")
        return False

    try:
        """
        문서를 자르고 임베딩 벡터를 생성합니다.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        # split documents
        all_splits = text_splitter.split_documents(documents)

        ### 라마 인덱스 index = VectorStoreIndex.from_documents(documents, show_progress=True)

        if not os.path.exists(embed_path):
            os.makedirs(embed_path)
        ### 라마 인덱스 old : index.storage_context.persist(persist_dir=embed_path)
        
        # store documents
        vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(),persist_directory=embed_path)
    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        return False
    return True


async def generate_recommendations() -> RecommendationOutput:
    """
    사용자가 물어볼 만한 적절한 질문을 파일 내용을 기반으로 생성합니다.
    """

    message = """
    주어진 문서에 대응하는 title, subtitle, description을 각각 작성해줘.
    """
    answer = await generate_message(question_message=message)
    description = answer.message

    logging.info("description text: \n%s", description)

    result = recommendation_agent(description=description)

    return result
