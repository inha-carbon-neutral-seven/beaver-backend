import logging

from typing import Optional

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai.chat_models import ChatOpenAI

from server.models.chart import ChartOutput, ChartType
from server.services.output_parsers.output_parsers import chart_parser
from server.services.storage import load_dataframe
from server.services.tools.tools import MemoryPythonAstREPLTool


CHART_SUFFIX = """
chart is based on the pre-prepared local pandas DataFrame 'df'.
Do not omit data by '...' in markdown format.
Do NOT use 'pyplot', 'pie()', 'plot' in python input.

This is the result of `print(df.head())`:
{df_head}

Your Final Answer should be in the format below in Korean:
{format_instruction}

Begin!
Question: {input}
{agent_scratchpad}
"""


def generate_chart(
    question: Optional[str] = None, chart_type: Optional[ChartType] = None
) -> ChartOutput | None:
    """
    데이터프레임을 기반으로 차트를 생성하는 Chain

    @Execution Time
    High

    @Method used
    ReAct, PythonREPL
    """
    logging.info("chart chain 실행...")

    df = load_dataframe()
    if df is None:
        logging.info("문서 파일은 차트를 제공하지 않음")
        return None

    if question is None:
        question = "csv 데이터를 대표하는 간단한 차트를 생성해 줘. 빠트린 정보가 있는지 엄격하게 검증해야 해. "

    if chart_type is not None:
        question += f"차트 타입은 {chart_type}로 해줘. "

    is_gpt_4 = True

    if is_gpt_4:
        model_name = "gpt-4-0125-preview"
    else:
        model_name = "gpt-3.5-turbo-0125"

    llm = ChatOpenAI(temperature=0.7, model_name=model_name)

    # agent 정의
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        suffix=CHART_SUFFIX,
        input_variables=["input", "df_head", "agent_scratchpad", "format_instruction"],
        include_df_in_prompt=None,  # True, 라이브러리 상 세팅으로 None 설정
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=8,
    )
    memory_python_repl_tool = MemoryPythonAstREPLTool(locals={"df": df})
    agent.tools = [memory_python_repl_tool]
    agent.handle_parsing_errors = True

    result = agent.invoke(
        {
            "input": question,
            "format_instruction": chart_parser.get_format_instructions(),
        }
    )

    output = result["output"]

    chart_output = chart_parser.parse(output)
    return chart_output
