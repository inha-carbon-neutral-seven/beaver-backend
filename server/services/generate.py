"""
POST /generate 
에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import logging
from operator import itemgetter

import pandas as pd
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.agents import create_pandas_dataframe_agent
from openai import APIConnectionError

from ..models.generate import Answer, AnswerType
from .storage import load_vectorstore, load_df_path


def generate_message(question_message: str) -> Answer:
    """
    LLM에 질문을 전달해 답변을 생성합니다.
    """
    logging.info("요청한 질문: %s", question_message)

    answer = None
    df_path = load_df_path()

    if df_path:
        answer = generate_message_from_table(question_message=question_message, df_path=df_path)
    else:
        answer = generate_message_from_document(question_message=question_message)

    logging.info("생성한 응답: %s", answer.message)
    return answer


def generate_message_from_table(question_message: str, df_path: str) -> Answer:
    df = pd.read_csv(df_path)

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=8,
    )

    logging.info("pandas dataframe agent 호출")

    response = agent.invoke({"input": question_message})
    # TODO: 가장 최근에 사용한 python input code를 클라이언트에게 전달할 것

    answer = Answer(
        type=AnswerType.TEXT,
        message=response["output"],
    )
    return answer


def generate_message_from_document(question_message: str) -> Answer:
    """
    문서로부터 답변을 생성합니다.
    """
    message = None

    vectorstore = load_vectorstore()
    if not vectorstore:
        message = "파일이 첨부되지 않았습니다."
        return Answer(
            type=AnswerType.TEXT,
            message=message,
        )

    try:
        logging.info("RAG starting...")
        # 벡터 유사도 검색
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

        # llm 정의
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

        # 템플릿 정의
        template = """You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.

        Context: {context}

        Question: {question}

        Answer in the following language: {language}"""

        custom_rag_prompt = PromptTemplate.from_template(template)

        def format_docs(docs):
            # TODO: top-k docs를 클라이언트에게 전달할 것
            return "\n\n".join(doc.page_content for doc in docs)

        # LCEL 정의
        rag_chain = (
            {
                "context": itemgetter("question") | retriever | format_docs,
                "question": itemgetter("question"),
                "language": itemgetter("language"),
            }
            | custom_rag_prompt
            | llm
            | StrOutputParser()
        )

        # 답변 생성
        message = rag_chain.invoke({"question": question_message, "language": "Korean"})
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
