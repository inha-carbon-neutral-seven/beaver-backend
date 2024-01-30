from operator import itemgetter
import json
from langchain_core.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from ..output_parsers.output_parsers import RecapOutput, RecommendationOutput, recommendation_parser


RECOMMENDATION_TEMPLATE = """Given the recap of the data {racap}
about a document from create THREE different specific questions that retailers might want to know about their data in Korean:
\n{format_instructions}"""


def lookup(recap_output: RecapOutput) -> RecommendationOutput:
    """
    임베딩 정보를 기반으로 사용자가 물어볼 만한 적절한 질문을 생성하는 Agent
    """
    recap = json.dumps(recap_output.to_dict())
    llm = ChatOpenAI(temperature=0.4, model_name="gpt-3.5-turbo")

    rag_prompt = PromptTemplate(
        input_variables=["racap"],
        template=RECOMMENDATION_TEMPLATE,
        partial_variables={
            "format_instructions": recommendation_parser.get_format_instructions(),
        },
    )

    # LCEL 정의
    rag_chain = (
        {
            "racap": itemgetter("racap"),
        }
        | rag_prompt
        | llm
        | recommendation_parser
    )

    recommendation_output = rag_chain.invoke(
        {"racap": recap},
    )

    return recommendation_output
