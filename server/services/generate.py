"""
POST /generate 
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import logging
from ..models.generate import Answer
from .storage import load_dataframe
from .agents import answer_table_agent, answer_document_agent


def generate_message(message_input: str) -> Answer:
    """
    LLM에 질문을 전달해 답변을 생성합니다.
    """
    logging.info("요청한 질문: %s", message_input)

    df = load_dataframe()

    if df is None:
        answer = answer_document_agent(message_input)
    else:
        answer = answer_table_agent(message_input, df)

    logging.info("생성한 응답: %s", answer.message)
    logging.info("생성한 소스: %s", answer.sources)

    return answer
