import logging
from llama_index import ServiceContext
from llama_index.output_parsers import LangchainOutputParser
from llama_index.llms import OpenAI
from server.services.output_parsers.output_parsers import (
    RecommendationOutput,
    recommendation_parser,
)
from server.services.storage import load_index


def generate_recommendation() -> RecommendationOutput | None:
    """
    Recap 정보를 기반으로 사용자가 물어볼 만한 적절한 질문을 생성하는 Chain

    @Execution Time
    Document : Medium
    Table    : Low

    @Method used
    RAG, tree_summarize
    """

    logging.info("recommendation chain 실행 ...")

    index = load_index()
    if index is None:
        return None
    service_context = _load_service_context()

    engine = index.as_query_engine(response_mode="tree_summarize", service_context=service_context)

    query_message = """You are a retailer. 
You want to ask a question to an AI chatbot that understands documents well.
Create three questions in Korean that can be asked after looking at the content."""

    res = engine.query(query_message)

    output_text = res.response
    recommendation_output = recommendation_parser.parse(output_text)
    return recommendation_output


def _load_service_context():

    # define output parser
    output_parser = LangchainOutputParser(recommendation_parser)

    llm = OpenAI(model="gpt-3.5-turbo-0125", output_parser=output_parser)
    service_context = ServiceContext.from_defaults(llm=llm)
    return service_context
