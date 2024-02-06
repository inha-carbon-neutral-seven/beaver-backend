import logging
from operator import itemgetter

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import APIConnectionError

from ..storage import load_vectorstore
from ...models.generate import AnswerType, Answer, IOMemory

RAG_TEMPLATE = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question in Korean. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {question}

Answer in Korean:"""


def lookup(message_input: str) -> Answer:
    """
    문서로부터 답변을 생성합니다.

    @Method used
    RAG
    """

    logging.info("document agent 호출")
    message = None
    sources = []

    vectorstore = load_vectorstore()

    if vectorstore is None:
        message = "파일이 첨부되지 않았습니다."
        return Answer(type=AnswerType.TEXT, message=message)

    # 벡터 유사도 검색
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # llm 정의
    if 1 == 1:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4-0125-preview")
    else:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo-0125")

    # 템플릿 정의
    custom_rag_prompt = PromptTemplate.from_template(RAG_TEMPLATE)

    def format_docs(docs):
        format_docs = "\n\n"
        for doc in docs:
            page_content = doc.page_content
            sources.append(IOMemory(output=str(page_content)))
            format_docs.join(page_content)
        return format_docs

    # LCEL 정의
    rag_chain = (
        {
            "context": itemgetter("question") | retriever | format_docs,
            "question": itemgetter("question"),
        }
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    try:
        message = rag_chain.invoke({"question": message_input})

    except APIConnectionError:
        logging.warning("모델 서버 이상: 토큰 초과 또는 연결 불가")
        message = "모델 서버 상태를 확인해주세요."

    return Answer(
        type=AnswerType.TEXT,
        message=message,
        sources=sources,
    )
