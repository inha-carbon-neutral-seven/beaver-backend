from fastapi import APIRouter

from ..services.embed import run
from ..models.embed import EmbedOutput

embed_router = APIRouter()


@embed_router.get("/embed")
async def embed() -> EmbedOutput:
    """
    인덱스를 모델 서버가 이해할 수 있는 형태로 임베딩합니다.
    """

    return run()
