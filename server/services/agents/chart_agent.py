import logging
from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from ...models.chart import ChartType, ChartOutput
from ..tools import MemoryPythonAstREPLTool
from ..output_parsers import chart_parser
from ..storage import load_dataframe

CHART_SUFFIX = """
The chart is based on the pre-prepared local pandas DataFrame 'df'. 
The length of data to be handled should be between 3 and 20. Also, don't create too much output.
Do not omit data by '...' in markdown format.
"bar" type chart will represent data in rectangular bars, helpful for comparing quantities across categories.
"pie" type chart will represent data in sectors of a circle, ideal for showing the proportion of parts against the whole.

This is the result of `print(df.head())`:
{df_head}

Your Final Answer should be in the format below in Korean:
{format_instruction}

Begin!
Question: {input}
{agent_scratchpad}
"""


def lookup(question: str = None, chart_type: ChartType = None) -> ChartOutput | None:
    """
    데이터프레임을 기반으로 차트를 생성하는 Agent

    @Execution Time
    Document : Not Executed
    Table    : High

    @Method used
    ReAct, PythonREPL
    """
    logging.info("chart agent 실행...")

    df = load_dataframe()
    if df is None:
        logging.info("문서 파일은 차트를 제공하지 않음")
        return None

    if question is None:
        question = "csv 데이터를 대표하는 간단한 차트를 생성해 줘. "

    if chart_type is not None:
        question += f"차트 타입은 {chart_type}로 해줘. "

    if 1 == 1:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4-0125-preview")
    else:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo-0125")

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        suffix=CHART_SUFFIX,
        input_variables=["input", "df_head", "agent_scratchpad", "format_instruction"],
        include_df_in_prompt=None,  # True, 라이브러리 상 세팅으로 None 설정
        verbose=True,
        max_iterations=8,
    )
    memory_python_repl_tool = MemoryPythonAstREPLTool(locals={"df": df})
    agent.handle_parsing_errors = True

    agent.tools = [memory_python_repl_tool]

    result = agent.invoke(
        {"input": question, "format_instruction": chart_parser.get_format_instructions()}
    )

    output = result["output"]

    chart_output = chart_parser.parse(output)
    logging.info("history in chart :: %s", memory_python_repl_tool.history)

    return chart_output
