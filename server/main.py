import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index import OpenAIEmbedding, ServiceContext, set_global_service_context
from llama_index.llms import OpenAI

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
async def load_openai():
    # env 설정
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    # 로그 설정
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    # 프롬프트 및 LLM 설정
    system_prompt = """당신은 AI 챗봇이며, 사용자에게 도움이 되는 유익한 내용을 제공해야 합니다.
    첨부한 자료를 근거로 해서 질문에 답해주시기 바랍니다. 
    대답은 짧게 생성해주세요. """
    llm = OpenAI(temperature=0, api_key=api_key, api_base=base_url, system_prompt=system_prompt)
    embed_model = OpenAIEmbedding(api_key=api_key, api_base=base_url)

    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    set_global_service_context(service_context=service_context)
