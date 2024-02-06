"""
저장 공간 관리에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import os
import logging
import json

from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pandas import read_csv
import pandas as pd

from .session import get_user_id
from ..models.recap import RecapOutput

TABLE_EXT = [".csv"]


def get_storage_path() -> str:
    """
    사용자의 저장소 경로를 가져옵니다.
    """
    user_id = get_user_id()
    storage_path = os.path.join("./server/storage", str(user_id))
    return storage_path


def _get_subdirectory_path(subdirectory_name: str) -> str:
    """
    사용자의 서브 디렉토리 경로를 가져옵니다.
    """
    storage_path = get_storage_path()
    return os.path.join(storage_path, subdirectory_name)


def get_document_path() -> str:
    """
    문서 경로를 가져옵니다.
    """
    return _get_subdirectory_path("document")


def get_recap_path() -> str:
    """
    요약 문서 경로를 가져옵니다.
    """
    return os.path.join(get_document_path(), "recap")


def get_table_path() -> str:
    """
    테이블 경로를 가져옵니다.
    """
    return _get_subdirectory_path("table")


def get_vectorstore_path() -> str:
    """
    벡터스토어 경로를 가져옵니다.
    """
    return _get_subdirectory_path("vectorstore")


def clear_storage() -> None:
    """
    저장소를 비웁니다.
    """
    storage_path = get_storage_path()
    document_path = get_document_path()
    vectorstore_path = get_vectorstore_path()
    table_path = get_table_path()
    recap_path = get_recap_path()

    # 기존 디렉토리 및 하위 내용 삭제
    if os.path.exists(storage_path):
        for root, dirs, files in os.walk(storage_path, topdown=False):
            for file_name in files:
                os.remove(os.path.join(root, file_name))
            for dir_name in dirs:
                os.rmdir(os.path.join(root, dir_name))
        os.rmdir(storage_path)

    #  디렉토리 재생성
    os.makedirs(storage_path)
    os.makedirs(document_path)
    os.makedirs(vectorstore_path)
    os.makedirs(table_path)
    os.makedirs(recap_path)


def save_file(contents: bytes, filename: str, description: str) -> None:
    """
    파일을 확장자에 맞추어 저장합니다.
    """

    # 확장자 추출
    _, file_ext = os.path.splitext(filename)
    new_filename = f"{description + file_ext}"

    if file_ext.lower() in TABLE_EXT:
        save_path = get_table_path()
    else:
        save_path = get_document_path()

    file_path = os.path.join(save_path, new_filename)

    with open(file_path, "wb") as fp:
        fp.write(contents)


def load_dataframe():
    """
    테이블 파일을 불러와 dataframe으로 전달합니다. 파일이 없다면 None을 반환합니다.
    """
    table_path = get_table_path()
    files_in_path = os.listdir(table_path)

    # 지원하는 확장자를 가진 파일 찾기
    table_filename = next(
        (file for file in files_in_path if any(file.endswith(ext) for ext in TABLE_EXT)), None
    )

    if not table_filename:
        return None

    # df 불러오기
    try:
        table_file = os.path.join(table_path, table_filename)
        df = read_csv(table_file)

    except FileNotFoundError:
        logging.warning("load_dataframe 함수를 호출했으나 데이터 프레임을 가져올 수 없음")
        return None

    # to_datetime 정적으로 formatting
    date_words = ["date", "time", "날짜", "일자"]

    for column in df.columns:
        if any(word in column.lower() for word in date_words):
            df[column] = pd.to_datetime(df[column], errors="ignore")

    return df


def get_splitted_documents(chunk_size=1000, chunk_overlap=0):
    """
    임베딩 또는 문서 요약에 사용하는 splitted documents를 가져옵니다.
    """
    document_path = get_document_path()
    try:
        # 디렉토리를 읽어옵니다. [Loader: UnstructuredFileLoader]
        loader = DirectoryLoader(document_path, show_progress=True)
        documents = loader.load()

    except ValueError:
        logging.warning("splitted documents 로딩 오류: 저장소를 읽을 수 없음")
        return []

    # 문서를 text_splitter로 자릅니다.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )
    splitted_documents = text_splitter.split_documents(documents)
    return splitted_documents


def load_vectorstore():
    """
    임베딩 vectorstore를 가져와 인덱스를 호출합니다.
    """
    vectorstore_path = get_vectorstore_path()

    try:
        vectorstore = FAISS.load_local(vectorstore_path, OpenAIEmbeddings())
        return vectorstore

    except (RuntimeError, ValueError) as e:  # 임베딩 파일이나 세션을 확인하지 못하는 경우
        logging.warning("vectorstore를 가져오지 못함: %s", e)
        return None


def save_recap(recap_output: RecapOutput) -> bool:
    recap_path = get_recap_path()
    file_path = os.path.join(recap_path, f"{recap_output.title}.txt")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(recap_output.model_dump(), f, indent=4, ensure_ascii=False)
        return True

    except OSError:
        logging.warning("recap save 오류: 파일스트림에 접근할 수 없음")
        return False


def load_recap() -> RecapOutput:
    recap_path = get_recap_path()
    file_path = None
    for file in os.listdir(recap_path):
        if file.endswith(".txt"):
            file_path = os.path.join(recap_path, file)

    try:
        if file_path is None:
            logging.warning("recap load 오류: recap 파일이 존재하지 않음")
            return RecapOutput()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return RecapOutput(**data)

    except OSError:
        logging.warning("recap load 오류: 파일스트림에 접근할 수 없음")
        return RecapOutput()
