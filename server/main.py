import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.embed import embed_router
from .routes.generate import generate_router
from .routes.ping import ping_router
from .routes.upload import upload_router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping_router)
app.include_router(upload_router)
app.include_router(embed_router)
app.include_router(generate_router)


@app.on_event("startup")
async def startup():
    # env 설정
    load_dotenv()
    if "OPENAI_API_BASE" not in os.environ and "OPENAI_BASE_URL" in os.environ:
        # OPENAI_BASE_URL을 OPENAI_API_BASE로 설정
        os.environ["OPENAI_API_BASE"] = os.environ.get("OPENAI_BASE_URL")

    # 로그 설정
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
