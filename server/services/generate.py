"""
POST /generate
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다.
"""

import logging

from konlpy.tag._okt import Okt

from ..models.generate import Answer, AnswerType
from .agents.answer_document_agent import lookup as answer_document_agent
from .agents.answer_table_agent import lookup as answer_table_agent
from .storage import load_dataframe


def generate_message(message_input: str) -> Answer:
    """
    LLM에 질문을 전달해 답변을 생성합니다.
    """
    logging.info("요청한 질문: %s", message_input)

    df = load_dataframe()

    if df is None:
        answer = answer_document_agent(message_input)

    else:
        is_visualization_request = filter_visualization_request(message_input)

        if is_visualization_request:
            answer_type = AnswerType.CHART
            logging.info("질문에서 시각화 요청 감지")

        else:
            answer_type = AnswerType.TEXT

        answer = answer_table_agent(df, message_input, answer_type)

    logging.info("생성한 응답: %s", answer.message)

    return answer


def filter_visualization_request(message_input: str) -> bool:
    """
    시각화를 요청하는 문장인지 표제어 추출(Lemmaization)을 통해 알아냅니다.
    """

    okt = Okt()
    morph_result = okt.pos(message_input, norm=True, stem=True)

    nouns = ["분석", "시각", "차트", "시각화", "통계", "동향", "변화", "요약", "생성", "인사이트"]
    verbs = ["보다", "그리다", "생성하다", "보여주다", "만들다"]

    word_dict = {}
    for noun in nouns:
        word_dict[noun] = 0

    for verb in verbs:
        word_dict[verb] = 1

    pos_code = {"Noun": 0, "Verb": 1, "Josa": 2, "Adjective": 3, "Suffix": 4}

    for word, pos in morph_result:
        if word in word_dict:
            a = word_dict[word]
            b = pos_code[pos]

            if a == b:
                return True

    return False
