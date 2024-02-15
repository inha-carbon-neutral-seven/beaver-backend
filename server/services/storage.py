"""
저장 공간 관리에 사용되는 비즈니스 로직을 담은 코드 페이지입니다.
"""

import logging
import os

import pandas as pd

from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore
from pandas import read_csv

from .session import get_user_id


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
    try:
        files_in_path = os.listdir(table_path)

    except FileNotFoundError:
        logging.warning("데이터 프레임을 가져올 수 없음")
        return None

    # 지원하는 확장자를 가진 파일 찾기
    table_filename = next(
        (file for file in files_in_path if any(file.endswith(ext) for ext in TABLE_EXT)), None
    )

    if not table_filename:
        return None

    # df 불러오기
    try:
        table_file = os.path.join(table_path, table_filename)

        # 지원되는 인코딩 찾기
        encodings = ["utf-8", "euc-kr"]
        for encoding in encodings:
            try:
                df = read_csv(table_file, encoding=encoding)
                break

            except UnicodeDecodeError:
                continue

        else:
            raise FileNotFoundError

    except FileNotFoundError:
        logging.warning("데이터 프레임을 가져올 수 없음")
        return None

    # to_datetime 정적으로 formatting
    date_words = ["date", "time", "날짜", "일자"]

    for column in df.columns:
        if any(word in column.lower() for word in date_words):
            df[column] = pd.to_datetime(df[column], errors="ignore")

    return df


def load_index() -> VectorStoreIndex | None:
    """
    VectorStoreIndex 를 불러옵니다.
    """
    vectorstore_path = get_vectorstore_path()

    # load index from disk
    try:
        vector_store = FaissVectorStore.from_persist_dir(vectorstore_path)

    except ValueError:
        logging.warning("index 불러오기 오류: vectorstore 파일을 확인할 수 없음")
        return None

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
        persist_dir=vectorstore_path,
    )

    index = load_index_from_storage(storage_context=storage_context)
    return index
