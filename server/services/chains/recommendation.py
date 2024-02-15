import logging

from llama_index import ServiceContext, SimpleDirectoryReader
from llama_index.llms import OpenAI
from llama_index.response_synthesizers import TreeSummarize

from server.models.recommendation import RecommendationOutput
from server.services.storage import get_document_path


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

    try:
        document_path = get_document_path()
        documents = SimpleDirectoryReader(document_path).load_data()

    except ValueError as e:
        logging.warning("파일이 첨부되지 않음: %s", e)
        return None

    document_text = documents[0].text

    service_context = _load_service_context()

    summarizer = TreeSummarize(
        service_context=service_context,
        output_cls=RecommendationOutput,
        verbose=True,
    )
    query_message = """You are a retailer.
You want to ask a question to an AI chatbot that understands documents well.
Create three questions in Korean that can be asked after looking at the content."""

    res = summarizer.get_response(query_str=query_message, text_chunks=[document_text])
    logging.info("recap result: %s", res.to_dict())

    return res


def _load_service_context():
    llm = OpenAI(model="gpt-3.5-turbo-0125")
    service_context = ServiceContext.from_defaults(llm=llm)
    return service_context
