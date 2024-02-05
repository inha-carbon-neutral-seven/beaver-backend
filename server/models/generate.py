from typing import Optional, List

from enum import Enum
from pydantic import BaseModel, Field
from .chart import ChartOutput


class AnswerType(str, Enum):
    TEXT = "text"
    CHART = "chart"


class Question(BaseModel):
    message: str = Field(description="사용자가 요청한 질문 텍스트입니다. ")


class Answer(BaseModel):
    type: AnswerType = Field(description="생성한 답변의 형식을 정의합니다. ")
    message: Optional[str] = Field(None, description="사용자의 질문에 대응하는 AI 챗봇의 답변 텍스트입니다. ")
    chart: Optional[ChartOutput] = Field(None, description="AI 챗봇이 만든 차트 데이터입니다. ",)
    sources: List[str] = Field([], description="답변에 사용한 근거를 제시합니다. ")

    def to_dict(self):
        return {
            "type": self.type,
            "message": self.message,
            "chart": self.chart,
            "sources": self.sources,
        }
