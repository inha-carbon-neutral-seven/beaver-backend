from fastapi import APIRouter, Form, UploadFile

from ..services.upload import upload_file


upload_router = APIRouter()


@upload_router.post("/upload")
async def upload(file: UploadFile = Form(...), description: str = Form(...)):
    """
    인덱스로 사용할 파일을 업로드합니다.
    """

    contents = await file.read()
    filename = file.filename.replace(" ", "-")
    description = description.replace(" ", "-")

    return upload_file(contents, filename, description)
