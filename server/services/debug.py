"""
debug 디버깅에 사용하는 비즈니스 로직을 담은 코드 페이지입니다.
/debug/{test_router} 양식을 가집니다.
"""

from asyncio import sleep
from typing import Any

from ..models.chart import ChartType
from ..models.generate import Answer, AnswerType, IOMemory
from ..models.process import ChartOutput, ProcessOutput, ProcessType, RecapOutput
from ..services.generate import filter_visualization_request
from .storage import load_dataframe


async def run_process(process_type: ProcessType, delay: int = 4) -> ProcessOutput:
    """
    프로세스 관련 서비스를 디버깅 합니다.
    """

    output: Any = None

    if process_type == ProcessType.RECAP:
        output = RecapOutput(
            title="월별 농축수산물 소매가격 테이블 데이터 분석",
            subtitle="품목 가격 및 유통 정보 분석",
            summary="""이 테이블은 소매업자가 제공한 데이터로, 총 25535개의 행과 8개의 열을 포함하고 있습니다.
주요 열은 '연도', '월', '품목명', '품종명', '평균가격', '등급명', '유통단계별무게', '유통단계별단위'입니다.
연도의 평균은 2013.43이며, 평균가격의 평균은 5693.59입니다.
유통단계별무게의 평균은 85.08이며, 최대값은 600입니다.
이 데이터를 통해 연도별 평균가격과 유통단계별무게의 변화를 분석할 수 있습니다.""",
            keywords=[
                "농축수산물",
                "데이터 분석",
                "품목명",
                "평균가격",
                "유통단계별무게",
                "연도",
            ],
        )

    elif process_type == ProcessType.CHART:
        delay = 10
        output = [
            ChartOutput(
                series=[{"name": "품목별 데이터 건수", "data": [1629, 1002, 862, 751, 697, 20594]}],
                labels=[
                    "쇠고기",
                    "오이",
                    "풋고추",
                    "건고추",
                    "호박",
                    "호박",
                    "이외 품목",
                ],
                title="품목명별 데이터 분포",
                type=ChartType.PIE,
            ),
        ]

    elif process_type == ProcessType.RECOMMENDATION:
        output = [
            "쇠고기의 평균 가격이 가장 높았던 시기는 언제인가요?",
            "등급에 따른 오이의 가격 차이는 얼마나 되나요?",
            "유통단계별무게가 100 이상인 제품은 어떤 품목들이 있나요?",
        ]

    else:
        output = None
        return ProcessOutput(status=False)

    await sleep(delay)

    return ProcessOutput(status=True, type=process_type, output=output)


async def run_generate(message_input: str, delay: int = 10) -> Answer:
    """
    LLM에 질문을 전달해 답변을 생성합니다.
    """
    question_1 = "쇠고기의 평균 가격이 가장 높았던 시기는 언제인가요?"
    answer_1 = (
        "쇠고기의 평균 가격이 가장 높았던 시기는 2022년 4월이며, 품종명은 한우안심이고, 등급명은 1+등급입니다. "
        + "평균 가격은 100g 당 19,458.182원이었습니다."
    )
    io_memory_1 = IOMemory(
        input="df[df['품목명'] == '쇠고기'].sort_values(by='평균가격', ascending=False).head(1)",
        output="         연도  월  품목명   품종명       평균가격   등급명  유통단계별무게 유통단계별단위\n"
        + "23602  2022  4  쇠고기  한우안심  19458.182  1+등급      100       g",
    )

    question_2 = "2024년 쇠고기 가격이 궁금해. 예상 결과를 보여줄 수 있어?"
    answer_2 = "2024년의 쇠고기 평균 가격을 선형 회귀 모델을 사용하여 약 8973원으로 예측하였습니다."
    io_memory_2 = IOMemory(
        input="from sklearn.linear_model import LinearRegression\n"
        + "import numpy as np\n"
        + "years = np.array([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])\n"
        + "prices = np.array([2559.493617, 2736.605401, 960.389374, 3282.544914, 3741.677062, "
        + "3840.397646, 5232.586336, 6793.148872, 7466.035397, 8197.025816, 8973.213920])\n"
        + "model = LinearRegression().fit(years, prices)\n"
        + "predicted_price_2024 = model.predict(np.array([[2024]]))\n"
        + "predicted_price_2024\n",
        output="[8973.21392028]",
    )

    if question_1 + question_2 is None:
        question_2 = None

    await sleep(delay)

    df = load_dataframe()

    if df is None:
        delay = 3
        answer = Answer(
            type=AnswerType.TEXT,
            message="문서 답변입니다.",
        )

    else:
        is_visualization_request = filter_visualization_request(message_input)

        if is_visualization_request:
            delay = 12
            answer_type = AnswerType.CHART

            chart = ChartOutput(
                title="2024년 쇠고기 평균 가격 예상",
                series=[
                    {
                        "name": "연도별 쇠고기 평균 가격",
                        "data": [
                            2559.493617,
                            2736.605401,
                            2960.389374,
                            3282.544914,
                            3741.677062,
                            3840.397646,
                            5232.586336,
                            6793.148872,
                            7466.035397,
                            8197.025816,
                            8973.213920,
                        ],
                    }
                ],
                labels=[
                    "2013",
                    "2014",
                    "2015",
                    "2016",
                    "2017",
                    "2018",
                    "2019",
                    "2020",
                    "2021",
                    "2022",
                    "2024 예상",
                ],
                type=ChartType.LINE,
            )

            answer = Answer(
                type=answer_type,
                message=answer_2,
                chart=chart,
                sources=[io_memory_2],
            )

        else:
            delay = 8
            answer_type = AnswerType.TEXT
            answer = Answer(
                type=answer_type,
                message=answer_1,
                sources=[io_memory_1],
            )

    return answer
