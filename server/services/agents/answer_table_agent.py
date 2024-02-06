import logging
from pandas import DataFrame
import pandas as pd
from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from ...models.generate import Answer, AnswerType
from ..tools import MemoryPythonAstREPLTool

TABLE_SUFFIX = """
Your Answer is based on the pre-prepared local pandas DataFrame 'df'.
and do NOT use pyplot.
This is the result of `print(df.head())`:
{df_head}

Your Final Answer should be in Korean:

Begin!
Question: {input}
{agent_scratchpad}
"""


def lookup(message_input: str, df: DataFrame) -> Answer:
    """
    테이블로부터 답변을 생성합니다.

    @Method used
    ReAct, PythonREPL
    """
    logging.info("table agent 호출")

    message = None
    sources = []

    if 1 == 1:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4-0125-preview")
    else:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo-0125")

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        suffix=TABLE_SUFFIX,
        input_variables=["input", "df_head", "agent_scratchpad"],
        include_df_in_prompt=None,
        verbose=True,
        max_iterations=8,
    )

    memory_python_repl_tool = MemoryPythonAstREPLTool(locals={"df": df, "pd": pd})
    agent.handle_parsing_errors = True

    agent.tools = [memory_python_repl_tool]

    result = agent.invoke({"input": message_input})

    message = result["output"]

    sources = memory_python_repl_tool.history

    answer = Answer(
        type=AnswerType.TEXT,
        message=message,
        sources=sources,
    )
    return answer
