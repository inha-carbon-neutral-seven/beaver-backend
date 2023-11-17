import logging

from fastapi import APIRouter
from openai import APIConnectionError
from llama_index import SimpleDirectoryReader, VectorStoreIndex

from ..models.ping import Pong

ping_router = APIRouter()


@ping_router.get("/ping")
async def ping():
    try:
        docs = SimpleDirectoryReader(
            input_dir="./server/static", recursive=True
        ).load_data()
        VectorStoreIndex.from_documents(docs)

    except APIConnectionError:
        logging.warning("모델 서버에 연결할 수 없음")
        return Pong(status=False)

    return Pong(status=True)
