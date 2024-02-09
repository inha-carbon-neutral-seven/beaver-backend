import logging
from langchain_core.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from ..storage import get_splitted_documents
from ..output_parsers import RecapOutput, recap_parser

MAP_PROMPT_TEMPLATE = """Write a concise summary of the following:

{text}

CONCISE SUMMARY in Korean:"""

REDUCE_PROMPT_TEMPLATE = """The following is set of summaries:

{text}

Take these and distill it into a final, very long, consolidated summary of the entire document. 
The title must indicate that it is a summary of document.

{format_instructions}

very long, consolidated FORMATTED SUMMARY in Korean:"""


def lookup() -> RecapOutput:
    """
    첨부한 파일에 대한 Recap을 생성하는 Agent

    @Execution Time
    Document : High
    Table    : Low

    @Method used
    map-reduce summarization
    """
    logging.info("recap agent 실행 ...")
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo-0125")

    splitted_documents = get_splitted_documents(chunk_size=2000)
    format_instructions = recap_parser.get_format_instructions()

    # Initialize templates

    map_prompt = PromptTemplate(
        input_variables=["text"],
        template=MAP_PROMPT_TEMPLATE,
    )
    combine_prompt = PromptTemplate(
        input_variables=["text"],
        template=REDUCE_PROMPT_TEMPLATE,
        partial_variables={"format_instructions": format_instructions},
    )

    chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        return_intermediate_steps=True,
        map_prompt=map_prompt,
        combine_prompt=combine_prompt,
        verbose=True,
    )

    result = chain.invoke({"input_documents": splitted_documents})

    output_text = result["output_text"]

    recap_output = recap_parser.parse(output_text)

    return recap_output
