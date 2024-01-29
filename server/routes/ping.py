from fastapi import APIRouter

from ..models.ping import Pong
from ..services.ping import check_server_status


ping_router = APIRouter()


@ping_router.get("/ping")
async def ping() -> Pong:
    status = check_server_status()
    return Pong(status=status)
