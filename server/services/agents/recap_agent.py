from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, RetrievalQAWithSourcesChain
from langchain.chains.summarize import load_summarize_chain

from ..output_parsers.output_parsers import RecapOutput, recap_parser


def lookup(description: str) -> RecapOutput:
    """
    주어진 description을 기반으로 사용자가 물어볼 만한 적절한 질문을 생성하는 Agent
    """
    llm = ChatOpenAI(temperature=0.6, model_name="gpt-3.5-turbo")

    recap_template = """
    summarize the documents in Korean:
    \n{format_instructions}
    """

    recap_prompt_template = PromptTemplate(
        template=recap_template,
        partial_variables={
            "format_instructions": recap_parser.get_format_instructions(),
        },
    )

    chain = RetrievalQAWithSourcesChain(
        llm=llm,
        prompt=recap_prompt_template,
        retriever=None,
        verbose=True,
    )
    raise NotImplementedError
    
    result = chain.run(description=description)

    return recap_parser.parse(result)
