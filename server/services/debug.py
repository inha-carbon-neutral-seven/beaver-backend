"""
debug 디버깅에 사용하는 비즈니스 로직을 담은 코드 페이지입니다. 
/debug/{test_router} 양식을 가집니다. 
"""
from asyncio import sleep

from ..models.process import ProcessType, ProcessOutput, RecapOutput, ChartOutput
from ..models.chart import ChartType


async def run_process(process_type: ProcessType, delay: int = 3) -> ProcessOutput:
    """
    프로세스 관련 서비스를 디버깅 합니다.
    """

    output = None

    await sleep(delay)

    if process_type == ProcessType.RECAP:
        output = RecapOutput(
            title="2023년 하반기 소매업계 이슈",
            subtitle="디지털 재설계, 비용 효율화, 챗GPT 정복 등 주요 이슈",
            summary="2023년 하반기 소매업계에서 주목해야 할 6가지 이슈는 디지털 재설계, 비용 효율화, 챗GPT 정복, 소비자의 소비패턴 변화와 대응 전략, 디지털화 실패 시 대처 방법, 비용구조 혁신 등입니다. 이를 통해 불확실성에 대응할 수 있는 체력을 키워야 합니다.",
            keywords=[
                "2023년 하반기",
                "소매업계",
                "디지털 재설계",
                "비용 효율화",
                "챗GPT 정복",
                "소비자의 소비패턴 변화",
                "디지털화 실패",
                "대처 방법",
                "비용구조 혁신",
            ],
        )

    elif process_type == ProcessType.CHART:
        output = [
            ChartOutput(
                series=[{"name": "Bottles Sold", "data": [381305, 325943, 158268, 156031, 154141]}],
                labels=[
                    "VODKA 80 PROOF",
                    "TEQUILA",
                    "WHISKEY LIQUEUR",
                    "CANADIAN WHISKIES",
                    "SPICED RUM",
                ],
                title="Top 5 Categories by Bottles Sold",
                type=ChartType.BAR,
            ),
            ChartOutput(
                series=[
                    {
                        "name": "카테고리별 판매량",
                        "data": [1787, 3122, 144, 1144, 13832, 158268, 1950, 114, 3527, 2336],
                    }
                ],
                labels=[
                    "100 PROOF VODKA",
                    "100% Agave Tequila",
                    "AMARETTO - IMPORTED",
                    "AMERICAN ALCOHOL",
                    "AMERICAN AMARETTO",
                    "WHISKEY LIQUEUR",
                    "WHITE CREME DE CACAO",
                    "WHITE CREME DE MENTHE",
                    "Whiskey Liqueur",
                    "White Rum",
                ],
                title="카테고리별 판매량",
                type=ChartType.PIE,
            ),
        ]

    elif process_type == ProcessType.RECOMMENDATION:
        output = [
            "2023년에 신규로 출시될 제품은 무엇인가요?",
            "소매업자들에게 가장 많이 추천되는 마케팅 전략은 무엇인가요?",
            "AI 기술을 활용한 GPT 모델은 소매업에 어떤 도움을 줄 수 있을까요?",
        ]

    else:
        output = None
        return ProcessOutput(status=False)

    return ProcessOutput(status=True, type=process_type, output=output)
