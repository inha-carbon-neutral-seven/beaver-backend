from fastapi import APIRouter, Form, UploadFile

from ..services.upload_service import upload_service
from ..services.embed_service import embed_service
from ..models.pong import Pong

upload_router = APIRouter()


@upload_router.post("/upload")
async def upload_file(file: UploadFile = Form(...), description: str = Form(...)):
    contents = await file.read()
    filename = file.filename.replace(" ", "-")

    return await upload_service(contents, filename, description)


@upload_router.get("/embed")
async def embed_file():
    status = await embed_service()
    return Pong(status=status)
