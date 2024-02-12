import logging

from llama_index import ServiceContext, SimpleDirectoryReader
from llama_index.llms import OpenAI
from llama_index.response_synthesizers import TreeSummarize

from server.models.recap import RecapOutput
from server.services.storage import get_document_path


def generate_recap() -> RecapOutput | None:
    """
    첨부한 파일에 대한 Recap을 생성하는 Chain

    @Execution Time
    Document : Medium
    Table    : Low

    @Method used
    RAG, tree_summarize
    """
    logging.info("recap chain 실행 ...")
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
        output_cls=RecapOutput,
        verbose=True,
    )

    query_message = "Create a Recap in Korean. Fill in the summary part abundantly."
    try:
        res = summarizer.get_response(query_str=query_message, text_chunks=[document_text])
        logging.info("recap result: %s", res.to_dict())

        return res
    except ValueError as eeee:
        print(f"{eeee=}")
        raise eeee


def _load_service_context():
    llm = OpenAI(model="gpt-3.5-turbo-0125")
    service_context = ServiceContext.from_defaults(llm=llm)
    return service_context
