import asyncio
import os
import logging

from openai import APIConnectionError
from fastapi import APIRouter, Form, HTTPException, UploadFile

from ..models.ping import Pong


upload_router = APIRouter()

STORAGE_DIRECTORY = "./server/storage"  # 이미지를 저장할 경로


@upload_router.post("/upload")
async def upload_file(
    file: UploadFile = Form(...),
    description: str = Form(...),
):
    if not os.path.exists(STORAGE_DIRECTORY):
        try:
            os.makedirs(STORAGE_DIRECTORY)
        except HTTPException:
            print()

    contents = await file.read()

    # 파일 업로드
    with open(os.path.join(STORAGE_DIRECTORY, file.filename), "wb") as fp:
        fp.write(contents)

    return {"filename": file.filename, "description": description}


@upload_router.get("/embed")
async def embed_file():
    if not os.path.exists(STORAGE_DIRECTORY):
        pong = Pong(status=False)
        return pong
    else:
        for root, dirs, files in os.walk(STORAGE_DIRECTORY):
            for file in files:
                file_path = os.path.join(root, file)
                vector_result = await do_embed(file_path)
                await asyncio.sleep(5)  # 테스트 코드, 임베드에 5초가 걸린다고 가정

        pong = Pong(status=True)
        return pong


async def do_embed(file_path: str):
    """
    APIConnectionError로 핸들링해주세요.
    """
    vector_result = ""
    logging.info("벡터 변환 결과 : %s", vector_result[0:10])
    return vector_result
