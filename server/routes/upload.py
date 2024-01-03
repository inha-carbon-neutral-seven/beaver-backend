from fastapi import APIRouter, Form, UploadFile, Request

from ..services.upload import upload_file
from ..services.embed import embed_file
from ..services.session import set_user_id

from ..models.pong import Pong

upload_router = APIRouter()


@upload_router.post("/upload")
async def upload(request: Request, file: UploadFile = Form(...), description: str = Form(...)):
    """
    인덱스로 사용할 파일을 업로드합니다.
    """

    set_user_id(request=request)

    contents = await file.read()
    filename = file.filename.replace(" ", "-")

    return await upload_file(contents, filename, description)


@upload_router.get("/embed")
async def embed(request: Request):
    """
    인덱스를 모델 서버가 이해할 수 있는 형태로 임베딩합니다.
    """

    set_user_id(request=request)
    status = await embed_file()
    return Pong(status=status)
