import asyncio
import os
import pickle

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
                # await asyncio.sleep(5)  # 테스트 코드, 임베드에 5초가 걸린다고 가정
                print(f"store vector result : {vector_result}")

        pong = Pong(status=True)
        return pong


async def do_embed(file_path: str):
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores.faiss import FAISS

    print(f"send embed request {file_path}")
    with open(file_path) as f:
        lines = f.read()

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=100
    )
    splitted_lines = text_splitter.split_text(lines)  # 1000자씩 나누어서 청크로 반환

    docsearch = FAISS.from_texts(
        texts=splitted_lines,
        embedding=OpenAIEmbeddings(),
    )

    vector_result = docsearch

    # Generate the save path based on the input file_path
    save_dir = os.path.dirname(file_path)
    print(f"save_dir : {save_dir}")
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"file_name : {file_name}")
    save_path = os.path.join(save_dir, f"{file_name}_embedded_vectors.pkl")
    print(f"save vector result : {save_path}")
    # Save the vectors to the dynamically generated file path using pickle
    with open(save_path, "wb") as save_file:
        pickle.dump(vector_result, save_file)

    return vector_result
