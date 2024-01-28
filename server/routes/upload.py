from fastapi import APIRouter, Form, Request, UploadFile

from ..services.session import set_user_id
from ..services.upload import upload_file


upload_router = APIRouter()


@upload_router.post("/upload")
async def upload(request: Request, file: UploadFile = Form(...), description: str = Form(...)):
    """
    인덱스로 사용할 파일을 업로드합니다.
    """

    set_user_id(request=request)

    contents = await file.read()
    filename = file.filename.replace(" ", "-")

    return upload_file(contents, filename, description)
