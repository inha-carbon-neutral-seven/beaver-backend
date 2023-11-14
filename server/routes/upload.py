import os

from fastapi import APIRouter, HTTPException, UploadFile


upload_router = APIRouter()

STORAGE_DIRECTORY = "./server/storage"  # 이미지를 저장할 경로


@upload_router.post("/upload")
async def upload_file(file: UploadFile):
    if not os.path.exists(STORAGE_DIRECTORY):
        try:
            os.makedirs(STORAGE_DIRECTORY)
        except OSError as e:
            raise HTTPException from e

    contents = await file.read()

    # 파일 업로드
    with open(os.path.join(STORAGE_DIRECTORY, file.filename), "wb") as fp:
        fp.write(contents)

    return {"filename": file.filename}


@upload_router.get("/embed")
async def embed_file():
    if not os.path.exists(STORAGE_DIRECTORY):
        return {"message": "no file"}
    else:
        for root, dirs, files in os.walk(STORAGE_DIRECTORY):
            for file in files:
                file_path = os.path.join(root, file)
                vector_result = await do_embed(file_path)
                print(f"store vector result : {vector_result}")
        return {"message": "embed completed"}


async def do_embed(file_path: str):
    print(f"send embed request {file_path}")
    vector_result = ""
    return vector_result
