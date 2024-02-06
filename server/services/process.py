"""
POST /process
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import logging
from pydantic import ValidationError
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.exceptions import OutputParserException

from .ping import check_server_status
from .storage import (
    get_vectorstore_path,
    get_splitted_documents,
    load_recap,
    save_recap,
    load_dataframe,
)
from .agents import recap_agent, recommendation_agent, chart_agent
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
                if not embed_document():
                    return ProcessOutput(status=False)

                output = None

            elif process_type == ProcessType.RECAP:
                # 첨부한 파일 또는 문서를 임베딩합니다.
                if not embed_document():
                    return ProcessOutput(status=False)

                output = recap_agent()
                save_recap(output)

            elif process_type == ProcessType.CHART:
                output = []
                pie_chart_output = chart_agent(chart_type=ChartType.PIE)

                if pie_chart_output is not None:
                    output = [pie_chart_output]

            elif process_type == ProcessType.RECOMMENDATION:
                output = []
                recap = load_recap()
                recommendation_output = recommendation_agent(recap_output=recap)
                recommendations = recommendation_output.recommendations

                if recommendations is not None:
                    output = recommendations

            else:
                output = None
                return ProcessOutput(status=False)

            # 에러 없이 성공했으므로 루프를 종료합니다.
            break

        except (ValidationError, ValueError, OutputParserException) as err:
            retries += 1
            logging.warning("OutputParserException iteration. [%s]", retries)

            # 최대 에러 횟수에 도달하면 실행을 종료합니다.
            if retries == max_retries:
                logging.warning("OutputParserException max iteration exceeded. \n%s", err)

                return ProcessOutput(status=False, type=process_type, output=output)

    return ProcessOutput(status=True, type=process_type, output=output)


def embed_document() -> bool:
    """
    저장소에 있는 파일을 모델 서버로 보내 임베딩 결과를 받아옵니다.

    @Execution Time
    Document : High
    Table    : Low
    """
    if load_dataframe() is not None:
        logging.info("문서 임베딩: 테이블 데이터는 임베딩하지 않음")
        return True

    vectorstore_path = get_vectorstore_path()
    splitted_documents = get_splitted_documents(chunk_size=1000, chunk_overlap=200)

    try:
        # 자른 문서를 임베딩하고 동시에 persist 합니다.
        vectorstore = FAISS.from_documents(splitted_documents, embedding=OpenAIEmbeddings())
        vectorstore.save_local(vectorstore_path)

    except ValueError:
        logging.warning("문서 임베딩 오류: 모델 서버에 연결할 수 없음")
        return False

    return True
