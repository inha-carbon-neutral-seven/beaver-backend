from fastapi import APIRouter
from ..services.generate_service import generate_service
from ..models.generate import Answer, Question

generate_router = APIRouter()

@generate_router.post("/generate")
async def generate_message(question: Question) -> Answer:
    return await generate_service(question)
