import logging

from openai import APIConnectionError
from llama_index import ServiceContext
from llama_index.llms import OpenAI

from ..storage import load_index
from ...models.generate import AnswerType, Answer, IOMemory


def lookup(message_input: str) -> Answer:
    """
    문서로부터 답변을 생성합니다.

    @Method used
    RAG
    """

    logging.info("document agent 호출")

    index = None
    message = None

    try:
        index = load_index()
    except FileNotFoundError:  # 사용자로부터 임베딩 파일을 받지 못했을 때 예외를 표출함
        message = "파일이 첨부되지 않았습니다."
        return Answer(type=AnswerType.TEXT, message=message)

    service_context = _load_service_context()
    engine = index.as_query_engine(service_context=service_context)

    try:
        message_input = f"Answer politely in Korean. {message_input}"
        res = engine.query(message_input)
        message = res.response

    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        message = "모델 서버 상태를 확인해주세요."

    sources = []

    for source_node in res.source_nodes:
        node = source_node.node
        text = node.text
        sources.append(IOMemory(output=text))

    return Answer(
        type=AnswerType.TEXT,
        message=message,
        sources=sources,
    )


def _load_service_context():

    llm = OpenAI(model="gpt-3.5-turbo-0125")
    service_context = ServiceContext.from_defaults(llm=llm)
    return service_context
