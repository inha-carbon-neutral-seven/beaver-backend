from .formatted_pydantic import FormattedPydanticOutputParser
from ...models.chart import ChartOutput
from ...models.recommendation import RecommendationOutput
from ...models.recap import RecapOutput


chart_parser = FormattedPydanticOutputParser(pydantic_object=ChartOutput)
recommendation_parser = FormattedPydanticOutputParser(pydantic_object=RecommendationOutput)
recap_parser = FormattedPydanticOutputParser(pydantic_object=RecapOutput)
