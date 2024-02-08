import logging
from llama_index import ServiceContext
from llama_index.output_parsers import LangchainOutputParser
from llama_index.llms import OpenAI
from ..output_parsers.output_parsers import RecommendationOutput, recommendation_parser
from ..storage import load_index


def lookup() -> RecommendationOutput | None:
    """
    Recap 정보를 기반으로 사용자가 물어볼 만한 적절한 질문을 생성하는 Agent

    @Execution Time
    Document : Low
    Table    : Low

    @Method used
    None
    """

    logging.info("recommendation agent 실행 ...")

    index = load_index()
    if index is None:
        return None
    service_context = _load_service_context()

    engine = index.as_query_engine(response_mode="tree_summarize", service_context=service_context)

    query_message = """
Generate THREE different abstract questions based on context that you might be curious about. 
The answer must be in the form of a question in the polite form ending with a question mark in Korean.
"""

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
