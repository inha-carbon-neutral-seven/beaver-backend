import logging

from openai import OpenAI, APIConnectionError
from fastapi import APIRouter
from ..models.generate import Answer, Question
from ..setting import Settings

generate_router = APIRouter()


@generate_router.post("/generate")
async def generate_message(question: Question):
    """
    모델 서버에 대답을 요청하여 클라이언트에게 전달합니다.
    또한, 대화 기록을 서버에 저장합니다.
    """
    client = OpenAI(
        api_key="empty",
        base_url=Settings().llm_server_URL,
    )
    messages = [
        {
            "role": "system",
            "content": "당신은 AI 챗봇이며, 사용자에게 도움이 되는 유익한 내용을 제공해야 합니다."
            + " 답변은 길고 자세하게 친절한 설명을 덧붙여 작성하세요.",
        },
    ]
    message = question.message
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        answer = Answer(message=response.choices[0].message.content)
    except APIConnectionError as e:
        logging.exception("%s : 모델 서버에 연결할 수 없습니다. 모델 서버 상태 또는 env 환경 변수를 확인해주세요. ", e)
        answer = Answer(message="모델 서버 상태를 확인해주세요.")

    logging.info("생성한 응답: %s", answer.message)
    return answer
