from langchain.output_parsers import PydanticOutputParser

from ...models.dashboard import DashboardOutput
from ...models.recommendation import RecommendationOutput

dashboard_parser: PydanticOutputParser[DashboardOutput] = PydanticOutputParser(
    pydantic_object=DashboardOutput
)
recommendation_parser: PydanticOutputParser[RecommendationOutput] = PydanticOutputParser(
    pydantic_object=RecommendationOutput
)
