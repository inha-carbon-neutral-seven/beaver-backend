import os
import logging

from fastapi import APIRouter, Form, UploadFile
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from openai import APIConnectionError

from ..models.ping import Pong


upload_router = APIRouter()

STORAGE_PATH = "./server/storage/user1"  # 저장 경로, 세션 별 관리를 위해 폴더 분리해둠


@upload_router.post("/upload")
async def upload_file(file: UploadFile = Form(...), description: str = Form(...)):
    raw_path = STORAGE_PATH + "/raw"

    # 기존 디렉토리 및 하위 내용 삭제
    if os.path.exists(STORAGE_PATH):
        for root, dirs, files in os.walk(STORAGE_PATH, topdown=False):
            for file_name in files:
                os.remove(os.path.join(root, file_name))
            for dir_name in dirs:
                os.rmdir(os.path.join(root, dir_name))
        os.rmdir(STORAGE_PATH)

    # raw_path 디렉토리 재생성
    os.makedirs(raw_path)

    contents = await file.read()
    filename = file.filename.replace(" ", "-")

    with open(os.path.join(raw_path, filename), "wb") as fp:
        fp.write(contents)

    return {"filename": filename, "description": description}


@upload_router.get("/embed")
async def embed_file():
    raw_path = STORAGE_PATH + "/raw"
    embed_path = STORAGE_PATH + "/embed"
    docs = []

    try:
        docs = SimpleDirectoryReader(input_dir=raw_path, recursive=True).load_data()
    except ValueError:
        logging.warning("저장소가 비어 있음")
        return Pong(status=False)

    try:
        index = VectorStoreIndex.from_documents(docs)
        if not os.path.exists(embed_path):
            os.makedirs(embed_path)
        index.storage_context.persist(persist_dir=embed_path)
    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        return Pong(status=False)

    return Pong(status=True)
