from fastapi import APIRouter
from ..services.ping import check_server_status
from ..models.pong import Pong

ping_router = APIRouter()


@ping_router.get("/ping")
async def ping() -> Pong:
    status = await check_server_status()
    return Pong(status=status)
