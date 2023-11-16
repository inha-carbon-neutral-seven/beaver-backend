import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv

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
app.include_router(generate_router)


@app.on_event("startup")
def startup_event():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.base_url = os.getenv("OPENAI_BASE_URL")
