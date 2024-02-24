import logging

import pandas as pd

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai.chat_models import ChatOpenAI
from pandas import DataFrame

from ...models.generate import Answer, AnswerType
from ..output_parsers.output_parsers import table_qa_parser
from ..tools.tools import MemoryPythonAstREPLTool


TABLE_SUFFIX = """
Your Answer is based on the pre-prepared local pandas DataFrame 'df'.

Check strictly at each step whether data is omitted in '...' format.
If you miss it, prepare to process the data in another way.

Do NOT use 'pyplot', 'pie()', 'plot' in python input.

This is the result of `print(df.head())`:
{df_head}

Your Final Answer should be one that contains your personal opinion and specific answers in Korean:

Begin!
Question: {input}
{agent_scratchpad}
"""

PREDICT_SUFFIX = """
you SHOULD use scikit-learn library for time-series analysis. `import scikit-learn`
"""

CHART_SUFFIX = """
Check strictly at each step whether data is omitted in '...' format.
If you miss it, prepare to process the data in another way.

DO NOT use 'pyplot', 'pie()', 'plot' in python input.

This is the result of `print(df.head())`:
{df_head}

Your Final Answer should be one that contains your personal opinion and specific answers in Korean:
{format_instruction}

Begin!
Question: {input}
{agent_scratchpad}
"""


def lookup(
    df: DataFrame,
    message_input: str,
    answer_type: AnswerType = AnswerType.TEXT,
    predict: bool = False,
) -> Answer:
    """
    테이블로부터 답변을 생성합니다.

    @Method used
    ReAct, PythonREPL
    """
    logging.info("table agent 호출")

    is_gpt_4 = True

    if is_gpt_4:
        model_name = "gpt-4-0125-preview"
    else:
        model_name = "gpt-3.5-turbo-0125"

    llm = ChatOpenAI(temperature=0.7, model_name=model_name)

    if answer_type == AnswerType.CHART:
        answer = table_qa_with_chart(df=df, llm=llm, message_input=message_input, predict=predict)
    else:
        answer = table_qa(df=df, llm=llm, message_input=message_input, predict=predict)

    return answer


def table_qa(df: DataFrame, llm: ChatOpenAI, message_input: str, predict: bool) -> Answer:
    suffix = TABLE_SUFFIX

    if predict is True:
        suffix = PREDICT_SUFFIX + suffix

    # agent 설정
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        suffix=suffix,
        input_variables=["input", "df_head", "agent_scratchpad"],
        include_df_in_prompt=None,
        verbose=True,
    )
    memory_python_repl_tool = MemoryPythonAstREPLTool(locals={"df": df, "pd": pd})
    agent.tools = [memory_python_repl_tool]
    agent.handle_parsing_errors = True

    # agent 실행
    result = agent.invoke({"input": message_input})

    # 결과물 추출
    message = result["output"]
    sources = memory_python_repl_tool.parse_last_history()

    answer = Answer(
        type=AnswerType.TEXT,
        message=message,
        sources=sources,
    )
    return answer


def table_qa_with_chart(
    df: DataFrame, llm: ChatOpenAI, message_input: str, predict: bool
) -> Answer:
    suffix = CHART_SUFFIX

    if predict is True:
        suffix = PREDICT_SUFFIX + suffix

    # agent 설정
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        suffix=CHART_SUFFIX,
        input_variables=["input", "df_head", "agent_scratchpad", "format_instruction"],
        include_df_in_prompt=None,  # True, 라이브러리 상 세팅으로 None 설정
        verbose=True,
        return_intermediate_steps=True,
    )
    memory_python_repl_tool = MemoryPythonAstREPLTool(locals={"df": df, "pd": pd})
    agent.tools = [memory_python_repl_tool]
    agent.handle_parsing_errors = True

    # agent 실행
    result = agent.invoke(
        {
            "input": f"{message_input}. 대답을 잘 표현하는 차트도 같이 만들어줘.",
            "format_instruction": table_qa_parser.get_format_instructions(),
        }
    )

    # output 추출
    table_qa_output = table_qa_parser.parse(result["output"])
    sources = memory_python_repl_tool.parse_last_history()

    answer = Answer(
        type=AnswerType.CHART,
        message=table_qa_output.ai_answer,
        chart=table_qa_output.chart,
        sources=sources,
    )
    return answer
