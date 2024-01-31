import json
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from ..output_parsers.output_parsers import RecapOutput, RecommendationOutput, recommendation_parser


# 프롬프트는 항상 다듬을 것
RECOMMENDATION_TEMPLATE = """SYSTEM: 당신은 맥락에 맞는 유용한 질문을 생성하는 AI 챗봇입니다.
맥락과 관련 있는 서로 다른 3개의 질문을 생성해내는 것이 당신의 목표입니다. 
소매업자 입장에서 궁금할 만한 내용을 질문으로 생성하세요. 질문은 한국어로 되어있으며 물음표로 끝나는 존댓말 양식을 가집니다.  

다음은 맥락입니다:
{text}

{format_instructions}
당신이 생성한 질문:"""


def lookup(recap_output: RecapOutput) -> RecommendationOutput:
    """
    임베딩 정보를 기반으로 사용자가 물어볼 만한 적절한 질문을 생성하는 Agent
    """
    recap = json.dumps(recap_output.to_dict())
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")

    rag_prompt = PromptTemplate(
        input_variables=["text"],
        template=RECOMMENDATION_TEMPLATE,
        partial_variables={
            "format_instructions": recommendation_parser.get_format_instructions(),
        },
    )

    chain = LLMChain(
        llm=llm,
        prompt=rag_prompt,
        verbose=True,
    )

    result = chain.invoke({"text": recap})
    output_text = result["text"]

    recommendation_output = recommendation_parser.parse(output_text)

    return recommendation_output
