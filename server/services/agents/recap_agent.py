from operator import itemgetter
from langchain_core.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from ..storage import load_vectorstore
from ..output_parsers.output_parsers import RecapOutput, recap_parser

RECAP_TEMPLATE = """Organize the title, flow, and main keywords of the document.
Answer in the language Korean. Context is below: 
```
{context}
```
\n{format_instructions}"""


def lookup() -> RecapOutput:
    """
    임베딩한 문서를 기반으로 요약 문서를 생성하는 Agent

    # 문제 1. 문서를 제대로 못 물어옴 ㅠ 용량이 작으면 통째로 첨부할 예정
    아래 링크로 리팩터링 예정
    see more at :
    https://python.langchain.com/docs/modules/data_connection/retrievers/multi_vector#summary
    """
    llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")

    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    rag_prompt = PromptTemplate(
        template=RECAP_TEMPLATE,
        input_variables=["context"],
        partial_variables={"format_instructions": recap_parser.get_format_instructions()},
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    question = "Organize the title, flow, and main keywords of the document."

    # LCEL 정의
    rag_chain = (
        {
            "context": itemgetter("question") | retriever | format_docs,
        }
        | rag_prompt
        | llm
        | recap_parser
    )

    recap_output = rag_chain.invoke(
        {"question": question},
    )

    return recap_output
