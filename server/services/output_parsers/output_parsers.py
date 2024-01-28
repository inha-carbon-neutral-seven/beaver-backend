from langchain.output_parsers import PydanticOutputParser

from ...models.chart import ChartOutput
from ...models.recommendation import RecommendationOutput
from ...models.recap import RecapOutput

chart_parser: PydanticOutputParser[ChartOutput] = PydanticOutputParser(pydantic_object=ChartOutput)
recommendation_parser: PydanticOutputParser[RecommendationOutput] = PydanticOutputParser(
    pydantic_object=RecommendationOutput
)
recap_parser: PydanticOutputParser[RecapOutput] = PydanticOutputParser(pydantic_object=RecapOutput)
