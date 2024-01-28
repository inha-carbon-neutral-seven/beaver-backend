from typing import Optional

from enum import Enum
from pydantic import BaseModel, Field


class AnswerType(str, Enum):
    TEXT = "text"
    CHART = "chart"


class Question(BaseModel):
    message: str = Field(description="사용자가 요청한 질문 텍스트입니다. ")


class Answer(BaseModel):
    type: Optional[AnswerType] = Field(description="AI 챗봇이 생성한 답변의 형식을 정의합니다. ")
    message: str = Field(description="사용자의 질문에 대응하는 AI 챗봇의 답변 텍스트입니다. ")

    def to_dict(self):
        return {
            "type": self.type,
            "message": self.message,
        }
