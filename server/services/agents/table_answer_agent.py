import logging
from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from ..storage import load_dataframe
from ..output_parsers import ChartOutput, chart_parser

CHART_SUFFIX = """
Your Final Answer should be in the format below in Korean:
{format_instruction}

Begin!
Question: {input}
{agent_scratchpad}"""


def lookup(question: str = None) -> ChartOutput | None:
    """
    데이터프레임을 기반으로 차트를 생성하는 Agent

    @Execution Time
    Document : Not Executed
    Table    : High
    """
    logging.info("chart agent 실행...")

    df = load_dataframe()
    if df is None:
        logging.info("문서 파일은 차트를 제공하지 않음")
        return None

    if question is None:
        question = "csv 데이터를 대표하는 아주 간단한 차트를 생성해 줘. "

    llm = ChatOpenAI(temperature=0.4, model_name="gpt-4-0125-preview")

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        suffix=CHART_SUFFIX,
        input_variables=["input", "agent_scratchpad", "format_instruction"],
        include_df_in_prompt=None,
        verbose=True,
        max_iterations=8,
    )

    result = agent.invoke(
        {"input": question, "format_instruction": chart_parser.get_format_instructions()}
    )

    output = result["output"]

    chart_output = chart_parser.parse(output)

    return chart_output
