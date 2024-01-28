from fastapi import APIRouter, Request

from ..services.embed import embed_file, generate_recommendations
from ..services.session import set_user_id

from ..models.embed import EmbedOutput
from ..models.recap import RecapOutput
from ..models.chart import ChartOutput, ChartType, Series

embed_router = APIRouter()


@embed_router.get("/embed")
async def embed(request: Request) -> EmbedOutput:
    """
    인덱스를 모델 서버가 이해할 수 있는 형태로 임베딩합니다.
    """

    set_user_id(request=request)

    # no-embed
    status = True | await embed_file()

    if status is False:
        result = EmbedOutput(status=False, recap=None, recommendations=None, chart=None)
        return result

    recap_example = RecapOutput(
        title="Document Title",
        subtitle="Additional information or subtopics",
        summary="Brief overview of the main content",
        keywords=["keyword1", "keyword2", "keyword3"],
    )
    charts_example = [
        ChartOutput(
            type=ChartType.LINE,
            title="Product Trends by Month",
            labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            series=[
                Series(
                    name="Product A",
                    data=[10, 41, 35, 51, 49, 62, 69, 91, 148],
                )
            ],
        ),
    ]
    answer = True | await generate_recommendations()

    result = EmbedOutput(
        status=True,
        recap=recap_example,
        recommendations=["mock 1", "mock 2", "mock 3"],
        charts=charts_example,
    )
    return result
