import logging
import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.agents.types import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent

from openai import APIConnectionError

from ..models.generate import Answer, Question
from .storage import load_table_filename, load_embed_index


async def generate_message(question: Question) -> Answer:
    """
    LLM에 질문을 전달해 답변을 생성합니다.
    """
    logging.info("요청한 질문: %s", question.message)

    answer = None
    table_filename = await load_table_filename()

    if table_filename is not None:
        answer = await generate_message_from_table(question=question)
    else:
        answer = await generate_message_from_document(question=question)

    logging.info("생성한 응답: %s", answer.message)
    return answer


async def generate_message_from_table(question: Question) -> Answer:
    table_filename = await load_table_filename()
    df = pd.read_csv(table_filename)

    llm = ChatOpenAI(temperature=0)
    agent = create_pandas_dataframe_agent(
        agent_type=AgentType.OPENAI_FUNCTIONS, llm=llm, df=df, verbose=True, extra_tools=[]
    )

    logging.info("pandas dataframe agent 호출")

    question.message = f"메타 데이터를 제외하고 대답해줘. {question.message}"
    res = agent.run(question.message)

    answer = Answer(message=res)
    return answer


async def generate_message_from_document(question: Question) -> Answer:
    index = None
    message = None

    index = await load_embed_index()
    if index is None:
        message = "파일이 첨부되지 않았습니다."
        return Answer(message=message)

    try:
        logging.info("query engine 호출")
        query_engine = index.as_query_engine()
        question.message = f"메타 데이터를 제외하고 대답해줘. {question.message}"
        res = query_engine.query(question.message)
        message = res.response

    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        message = "모델 서버 상태를 확인해주세요."

    return Answer(message=message)
