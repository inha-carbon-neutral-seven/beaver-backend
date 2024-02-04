"""
직접 작성하는 사용자 지정 툴
agent 가 tool 의 docstring 을 읽고 적합한 툴인지 reasoning 함
"""

from ..output_parsers import ChartOutput

from ..agents import chart_agent


def create_chart(question: str) -> ChartOutput:
    """
    차트를 생성합니다.
    """
    chart_output = chart_agent(question)
    return chart_output
