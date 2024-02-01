"""
GET /embed
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import logging
from typing import Any
from pydantic import ValidationError
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.exceptions import OutputParserException

from .ping import check_server_status
from .storage import get_vectorstore_path, get_splitted_documents, load_recap, save_recap
from .agents import recap_agent, recommendation_agent, chart_agent
from ..models.process import ProcessType, ProcessInput, ProcessOutput


def run(process_input: ProcessInput) -> ProcessOutput:
    """
    임베딩 관련 서비스를 실행합니다.
    """

    # 모델 서버가 불안정하면 임베딩을 진행하지 않습니다.
    if not check_server_status():
        return ProcessOutput(status=False)

    process_type = process_input.type
    error_iter = 0
    max_error_iter = 2
    output: Any

    while error_iter < max_error_iter:
        try:
            if process_type == ProcessType.RECAP:
                # 첨부한 파일 또는 문서를 임베딩합니다.
                if not embed_document():
                    return ProcessOutput(status=False)

                output = recap_agent()
                save_recap(output)

            elif process_type == ProcessType.RECOMMENDATION:
                recap = load_recap()
                recommendation_output = recommendation_agent(recap_output=recap)
                output = recommendation_output.recommendations

            elif process_type == ProcessType.CHART:
                chart_output = chart_agent()
                if chart_output is not None:
                    output = [chart_output]

            else:
                return ProcessOutput(status=False)

            # 에러 없이 성공했으므로 루프를 종료합니다.
            break

        except (ValidationError, ValueError, OutputParserException) as err:
            error_iter += 1
            logging.warning("Pydantic ValidationError iteration. [%s]", error_iter)

            # 최대 에러 횟수를 초과하면 함수를 종료합니다.
            if error_iter >= max_error_iter:
                logging.warning("Pydantic ValidationError max iteration exceeded. \n%s", err)

                return ProcessOutput(status=False, type=process_type, output=output)

    return ProcessOutput(status=True, type=process_type, output=output)


def embed_document() -> bool:
    """
    저장소에 있는 파일을 모델 서버로 보내 임베딩 결과를 받아옵니다.

    @Execution Time
    Document : High
    Table    : Low
    """

    vectorstore_path = get_vectorstore_path()
    splitted_documents = get_splitted_documents()

    try:
        # 자른 문서를 임베딩하고 동시에 persist 합니다.
        vectorstore = FAISS.from_documents(splitted_documents, embedding=OpenAIEmbeddings())
        vectorstore.save_local(vectorstore_path)

    except ValueError:
        logging.warning("문서 임베딩 오류: 모델 서버에 연결할 수 없음")
        return False

    return True
