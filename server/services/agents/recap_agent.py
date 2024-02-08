import logging


from llama_index import ServiceContext
from llama_index.output_parsers import LangchainOutputParser
from llama_index.llms import OpenAI

from ..storage import load_index
from ..output_parsers.output_parsers import RecapOutput, recap_parser


def lookup() -> RecapOutput:
    """
    첨부한 파일에 대한 Recap을 생성하는 Agent

    @Execution Time
    Document : High
    Table    : Low

    @Method used
    map-reduce summarization
    """
    logging.info("recap agent 실행 ...")

    index = load_index()
    service_context = _load_service_context()

    engine = index.as_query_engine(response_mode="tree_summarize", service_context=service_context)
    query_message = """
    Create a Recap according to the instructions in Korean. 
    Fill in the summary part abundantly."""

    res = engine.query(query_message)

    output_text = res.response

    recap_output = recap_parser.parse(output_text)
    print(f"{recap_output}")
    return recap_output


def _load_service_context():

    # define output parser
    output_parser = LangchainOutputParser(recap_parser)

    llm = OpenAI(model="gpt-3.5-turbo-0125", output_parser=output_parser)
    service_context = ServiceContext.from_defaults(llm=llm)
    return service_context
