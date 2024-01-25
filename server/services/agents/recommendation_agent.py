from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from ..output_parsers.output_parsers import RecommendationOutput, recommendation_parser


def lookup(description: str) -> RecommendationOutput:
    """
    주어진 description을 기반으로 사용자가 물어볼 만한 적절한 질문을 생성하는 Agent
    """
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")

    recommendation_template = """
    Given the description {description}
    about a document from create THREE different specific questions that retailers might want to know about their data in Korean:
    Strictly follow the question format with question marks.
    \n{format_instructions}
    """

    # TODO: FewShotPromptTemplate 로 바꿀 것

    recommendation_prompt_template = PromptTemplate(
        input_variables=["description"],
        template=recommendation_template,
        partial_variables={
            "format_instructions": recommendation_parser.get_format_instructions(),
        },
    )

    chain = LLMChain(
        llm=llm,
        prompt=recommendation_prompt_template,
    )

    result = chain.run(description=description)

    return recommendation_parser.parse(result)
