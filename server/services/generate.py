"""
POST /generate 
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""
import logging

import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_experimental.agents import create_pandas_dataframe_agent
from openai import APIConnectionError

from ..models.generate import Answer, AnswerType
from .storage import load_embed_index, load_table_filename


async def generate_message(question_message: str) -> Answer:
    """
    LLM에 질문을 전달해 답변을 생성합니다.
    """
    logging.info("요청한 질문: %s", question_message)

    answer = None
    table_filename = await load_table_filename()

    if table_filename is not None:
        answer = await generate_message_from_table(
            question_message=question_message,
            pandas_dataframe_filename=table_filename,
        )
    else:
        answer = await generate_message_from_document(question_message=question_message)

    logging.info("생성한 응답: %s", answer.message)
    return answer


async def generate_message_from_table(
    question_message: str, pandas_dataframe_filename: str
) -> Answer:
    df = pd.read_csv(pandas_dataframe_filename)

    llm = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )
    agent.handle_parsing_errors = True

    logging.info("pandas dataframe agent 호출")

    response = agent.invoke({"input": question_message})
    answer = Answer(
        type=AnswerType.TEXT,
        message=response["output"],
    )
    return answer


async def generate_message_from_document(question_message: str) -> Answer:
    """
    문서로부터 답변을 생성합니다.
    """
    message = None

    vectorstore = await load_embed_index()
    if vectorstore is None:
        message = "파일이 첨부되지 않았습니다."
        return Answer(
            type=AnswerType.TEXT,
            message=message,
        )

    try:
        logging.info("RAG starting...")
        # 벡터 유사도 검색
        retriever = vectorstore.as_retriever(search_type="similarity", 
                                             search_kwargs={"k": 3})
        

        # llm 정의
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        # 템플릿 정의
        template = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.

        Context: {context}

        Question: {question}

        Answer: in Korean"""

        custom_rag_prompt = PromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # LCEL 정의
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | custom_rag_prompt
            | llm
            | StrOutputParser()
        )

        # 답변 생성
        message = "" 
        for chunk in rag_chain.stream(question_message):
            message += chunk
        
        logging.info("Answer: message")
        logging.info("RAG finished")

    except APIConnectionError:
        logging.warning("1. 토큰 초과 버그")
        logging.warning("2. 모델 서버에 연결할 수 없음")
        message = "모델 서버 상태를 확인해주세요."

    return Answer(
        type=AnswerType.TEXT,
        message=message,
    )
