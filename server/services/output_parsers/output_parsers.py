from ...models.chart import ChartOutput
from ...models.generate import TableQA
from ...models.recap import RecapOutput
from ...models.recommendation import RecommendationOutput
from ..output_parsers.formatted_pydantic import FormattedPydanticOutputParser


chart_parser: FormattedPydanticOutputParser[ChartOutput] = FormattedPydanticOutputParser(
    pydantic_object=ChartOutput
)
recommendation_parser: FormattedPydanticOutputParser[
    RecommendationOutput
] = FormattedPydanticOutputParser(pydantic_object=RecommendationOutput)
recap_parser: FormattedPydanticOutputParser[RecapOutput] = FormattedPydanticOutputParser(
    pydantic_object=RecapOutput
)
table_qa_parser: FormattedPydanticOutputParser[TableQA] = FormattedPydanticOutputParser(
    pydantic_object=TableQA
)
