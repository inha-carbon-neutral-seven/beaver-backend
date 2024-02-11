import logging
from llama_index import ServiceContext, SimpleDirectoryReader
from llama_index.llms import OpenAI
from llama_index.response_synthesizers import TreeSummarize
from server.services.storage import get_document_path
from server.models.recap import RecapOutput


def generate_recap() -> RecapOutput:
    """
    첨부한 파일에 대한 Recap을 생성하는 Chain

    @Execution Time
    Document : Medium
    Table    : Low

    @Method used
    RAG, tree_summarize
    """
    logging.info("recap chain 실행 ...")

    document_path = get_document_path()
    documents = SimpleDirectoryReader(document_path).load_data()

    document_text = documents[0].text

    service_context = _load_service_context()

    summarizer = TreeSummarize(
        service_context=service_context,
        output_cls=RecapOutput,
        verbose=True,
    )

    query_message = "Create a Recap in Korean. Fill in the summary part abundantly."

    res = summarizer.get_response(query_str=query_message, text_chunks=[document_text])
    logging.info("recap result: %s", res.to_dict())

    return res


def _load_service_context():

    llm = OpenAI(model="gpt-3.5-turbo-0125")
    service_context = ServiceContext.from_defaults(llm=llm)
    return service_context
