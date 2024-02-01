"""
GET /embed
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import logging

from pydantic import ValidationError
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.exceptions import OutputParserException

from .ping import check_server_status
from .storage import get_vectorstore_path, get_splitted_documents
from .agents.recap_agent import lookup as recap_agent, RecapOutput
from .agents.recommendation_agent import lookup as recommendation_agent
from .agents.chart_agent import lookup as chart_agent, ChartOutput
from ..models.embed import EmbedOutput


def run() -> EmbedOutput:
    """
    임베딩 관련 서비스를 실행합니다. 
    """
    # 모델 서버가 불안정하면 임베딩을 진행하지 않습니다.
    if not check_server_status():
        return EmbedOutput(status=False)

    # 첨부한 파일 또는 문서를 임베딩합니다.
    if not embed_document():
        return EmbedOutput(status=False)

    recap: RecapOutput = None
    recommendations: list[str] = []
    charts: list[ChartOutput] = []

    error_iter = 0
    max_error_iter = 5

    while error_iter < max_error_iter:
        try:
            # LLM으로부터 recap을 생성합니다.
            if not recap:
                recap = recap_agent()
                logging.info("생성한 recap: %s, ...", recap.summary)

            # LLM으로부터 list of recommendation을 생성합니다.
            if not recommendations:
                recommendation_output = recommendation_agent(recap_output=recap)
                recommendations = recommendation_output.recommendations
                logging.info("생성한 recommendations: %s, ...", recommendations[0])

            # list of chart를 생성합니다. (현재 example)
            if not charts:
                chart = chart_agent()
                if isinstance(chart, ChartOutput):
                    charts.append(chart)

                logging.info("생성한 charts: %s, ...", charts)

            # 에러 없이 모두 성공했으므로 루프를 종료합니다.
            break

        except (ValidationError, ValueError, OutputParserException) as err:
            error_iter += 1
            logging.warning("Pydantic ValidationError iteration. [%s]", error_iter)

            # 최대 에러 횟수를 초과하면 함수를 종료합니다.
            if error_iter >= max_error_iter:
                logging.warning("Pydantic ValidationError max iteration exceeded. \n%s", err)

                return EmbedOutput(
                    status=False,
                    recap=recap,
                    recommendations=recommendations,
                    charts=charts,
                )

    result = EmbedOutput(
        status=True,
        recap=recap,
        recommendations=recommendations,
        charts=charts,
    )
    return result


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
