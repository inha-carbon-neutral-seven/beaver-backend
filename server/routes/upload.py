from fastapi import APIRouter, Form, UploadFile

from ..services.upload_service import upload_file
from ..services.embed_service import embed_file
from ..models.pong import Pong

upload_router = APIRouter()


@upload_router.post("/upload")
async def upload(file: UploadFile = Form(...), description: str = Form(...)):
    """
    인덱스로 사용할 파일을 업로드합니다.
    """
    contents = await file.read()
    filename = file.filename.replace(" ", "-")

    return await upload_file(contents, filename, description)


@upload_router.get("/embed")
async def embed():
    """
    인덱스를 모델 서버가 이해할 수 있는 형태로 임베딩합니다.
    """
    status = await embed_file()
    return Pong(status=status)
