"""
저장 공간 관리에 사용되는 비즈니스 로직을 담은 코드 페이지입니다. 
"""

import os

from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings


from .session import get_user_id


TABLE_EXT = [".csv", ".tsv", ".xlsx"]


def get_storage_path() -> str:
    """
    storage path를 가져옵니다.
    """
    user_id = get_user_id()
    storage_path = os.path.join("./server/storage", str(user_id))
    return storage_path


def clear_storage() -> None:
    """
    저장소를 비웁니다.
    """
    storage_path = get_storage_path()
    document_path = os.path.join(storage_path, "document")
    chroma_path = os.path.join(storage_path, "chroma")
    table_path = os.path.join(storage_path, "table")

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

    file_path = None
    file_ext = None
    storage_path = get_storage_path()

    # 확장자 추출
    _, file_ext = os.path.splitext(filename)
    new_filename = f"{description}{file_ext}"

    if file_ext.lower() in TABLE_EXT:
        file_path = os.path.join(storage_path, "table", new_filename)
    else:
        file_path = os.path.join(storage_path, "document", new_filename)

    with open(file_path, "wb") as fp:
        fp.write(contents)


def load_table_filename() -> str | None:
    """
    path에 있는 첫 번째 테이블 파일 경로를 전달하는 함수
    """
    storage_path = get_storage_path()
    table_path = os.path.join(storage_path, "table")

    files = os.listdir(table_path)

    # 지원하는 확장자를 가진 파일 찾기
    table_file = next(
        (file for file in files if any(file.endswith(ext) for ext in TABLE_EXT)), None
    )

    if not table_file:
        return None

    table_file_path = os.path.join(table_path, table_file)

    return table_file_path


def load_vectorstore() -> Chroma | None:
    """
    임베딩 벡터 데이터를 가져와 인덱스를 호출합니다.
    """
    storage_path = get_storage_path()
    chroma_path = os.path.join(storage_path, "chroma")

    try:
        vectorstore = Chroma(persist_directory=chroma_path, embedding_function=OpenAIEmbeddings())

        return vectorstore
    except FileNotFoundError:  # 사용자로부터 임베딩 파일을 받지 못했을 때 예외를 표출함
        return None
