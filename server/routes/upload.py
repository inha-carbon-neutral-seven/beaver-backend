from fastapi import APIRouter


upload_router = APIRouter()


@upload_router.post("/upload")
async def upload_file():
    """
    파일을 업로드합니다.
    """
    return {"upload": True}


@upload_router.get("/embed")
async def embed_file():
    """
    파일 임베딩이 완료되었는지 확인합니다.
    """
    # 만약 업로드 파일이 없다면, false를 return
    # 만약 업로드 파일이 있는데 임베딩 파일이 없다면, 요청을 보내고, 응답이 오면 true를 return
    # 만약 업로드 파일과 임베딩 파일이 모두 있다면 true를 return
    return {"embed": True}
