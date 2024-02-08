"""
POST /process
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import logging

import faiss
from pydantic import ValidationError
from langchain_core.exceptions import OutputParserException
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore

from .ping import check_server_status
from .storage import get_vectorstore_path, get_document_path
from .agents.chart_agent import lookup as chart_agent
from .agents.recap_agent import lookup as recap_agent
from .agents.recommendation_agent import lookup as recommendation_agent
from ..models.process import ProcessType, ProcessOutput
from ..models.chart import ChartType


def run(process_type: ProcessType, max_retries: int = 2) -> ProcessOutput:
    """
    임베딩 관련 서비스를 실행합니다.
    """

    output = None

    # 모델 서버가 불안정하면 임베딩을 진행하지 않습니다.
    if not check_server_status():
        return ProcessOutput(status=False)

    retries = 0
    while retries < max_retries:
        try:
            if process_type == ProcessType.EMBED:
                # 첨부한 파일 또는 문서를 임베딩합니다.
                if not _embed_document():
                    return ProcessOutput(status=False)

                output = None

            elif process_type == ProcessType.RECAP:
                if not _embed_document():
                    return ProcessOutput(status=False)

                output = recap_agent()

            elif process_type == ProcessType.CHART:
                output = []
                pie_chart_output = chart_agent(chart_type=ChartType.PIE)

                if pie_chart_output is not None:
                    output = [pie_chart_output]

            elif process_type == ProcessType.RECOMMENDATION:
                output = []
                recommendation_output = recommendation_agent()

                if recommendation_output is None:
                    return ProcessOutput(status=False)

                output = recommendation_output.recommendations

            else:
                output = None
                return ProcessOutput(status=False)

            # 에러 없이 성공했으므로 루프를 종료합니다.
            break

        except RuntimeError as err:
            retries += 1
            logging.warning("OutputParserException iteration. [%s]", retries)

            # 최대 에러 횟수에 도달하면 실행을 종료합니다.
            if retries == max_retries:
                logging.warning("OutputParserException max iteration exceeded. \n%s", err)

                return ProcessOutput(status=False, type=process_type, output=output)

    return ProcessOutput(status=True, type=process_type, output=output)


def _embed_document() -> bool:

    # dimensions of text-ada-embedding-002
    d = 1536
    faiss_index = faiss.IndexFlatL2(d)

    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    try:
        document_path = get_document_path()
        documents = SimpleDirectoryReader(document_path).load_data()

    except FileNotFoundError:  # 사용자로부터 파일을 받지 못했을 때 예외를 표출함
        return False

    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    # save index to disk
    vectorstore_path = get_vectorstore_path()
    index.storage_context.persist(persist_dir=vectorstore_path)
    return True
