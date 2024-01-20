from fastapi import APIRouter, Request

from ..services.embed import embed_file
from ..services.session import set_user_id

from ..models.ping import Pong

embed_router = APIRouter()


@embed_router.get("/embed")
async def embed(request: Request):
    """
    인덱스를 모델 서버가 이해할 수 있는 형태로 임베딩합니다.
    """

    set_user_id(request=request)
    status = await embed_file()
    return Pong(status=status)
