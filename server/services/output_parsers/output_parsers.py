from ...models.chart import ChartOutput
from ...models.recap import RecapOutput
from ...models.recommendation import RecommendationOutput
from .formatted_pydantic import FormattedPydanticOutputParser


chart_parser: FormattedPydanticOutputParser[ChartOutput] = FormattedPydanticOutputParser(
    pydantic_object=ChartOutput
)
recommendation_parser: FormattedPydanticOutputParser[
    RecommendationOutput
] = FormattedPydanticOutputParser(pydantic_object=RecommendationOutput)
recap_parser: FormattedPydanticOutputParser[RecapOutput] = FormattedPydanticOutputParser(
    pydantic_object=RecapOutput
)
