from llama_index import OpenAIEmbedding, SimpleDirectoryReader, VectorStoreIndex
from openai import APIConnectionError

from fastapi import APIRouter, HTTPException

from ..models.ping import Pong


ping_router = APIRouter()


@ping_router.get("/ping")
async def ping():
    OpenAIEmbedding(timeout=5)
    try:
        docs = SimpleDirectoryReader(
            input_dir="./server/static", recursive=True
        ).load_data()
        VectorStoreIndex.from_documents(docs)

    except APIConnectionError:
        raise HTTPException(status_code=502, detail="모델 서버에 연결할 수 없음")

    return Pong(status=True)
