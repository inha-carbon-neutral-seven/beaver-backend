import logging
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.types import AgentType


from ..models.generate import Answer, Question
from .storage_service import load_csv_file


async def generate_message(question: Question) -> Answer:
    logging.info("요청한 질문: %s", question.message)

    try:
        csv_file = await load_csv_file()
    except FileNotFoundError as e:
        logging.warning("파일 로드 중 예외 발생: %s", e)
        return Answer(message="CSV 파일을 첨부하지 않았습니다.")

    df = pd.read_csv(csv_file)

    llm = ChatOpenAI(temperature=0)
    agent = create_pandas_dataframe_agent(
        agent_type=AgentType.OPENAI_FUNCTIONS, llm=llm, df=df, verbose=True, extra_tools=[]
    )

    res = agent.run(question.message)

    answer = Answer(message=res)
    logging.info("생성한 응답: %s", answer.message)
    return answer
