from fastapi import APIRouter
from ..services.ping_service import ping_service
from ..models.pong import Pong

ping_router = APIRouter()


@ping_router.get("/ping")
async def ping() -> Pong:
    status = await ping_service()
    return Pong(status=status)
