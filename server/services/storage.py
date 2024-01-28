"""
저장 공간 관리에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import os
import logging

from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from .session import get_user_id


TABLE_EXT = [".csv", ".tsv", ".xlsx"]


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


def get_chroma_path() -> str:
    """
    크로마 벡터스토어 경로를 가져옵니다.
    """
    return _get_subdirectory_path("chroma")


def clear_storage() -> None:
    """
    저장소를 비웁니다.
    """
    storage_path = get_storage_path()
    document_path = get_document_path()
    chroma_path = get_chroma_path()
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
    os.makedirs(chroma_path)
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


def load_table_filename() -> str | None:
    """
    path에 있는 첫 번째 테이블 파일 경로를 전달하는 함수
    """
    table_path = get_table_path()
    files_in_path = os.listdir(table_path)

    # 지원하는 확장자를 가진 파일 찾기
    table_file = next(
        (file for file in files_in_path if any(file.endswith(ext) for ext in TABLE_EXT)), None
    )

    if not table_file:
        return None

    file_path = os.path.join(table_path, table_file)
    return file_path


def load_vectorstore() -> Chroma | None:
    """
    임베딩 벡터 데이터를 가져와 인덱스를 호출합니다.
    """
    chroma_path = get_chroma_path()

    try:
        vectorstore = Chroma(persist_directory=chroma_path, embedding_function=OpenAIEmbeddings())
        return vectorstore

    except ValueError:  # 임베딩 파일이나 세션을 확인하지 못하는 경우
        logging.warn("vectorstore를 가져오지 못함")
        return None
