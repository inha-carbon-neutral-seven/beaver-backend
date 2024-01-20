from pydantic import BaseModel, Field


class Question(BaseModel):
    message: str = Field(description="사용자가 요청한 질문 텍스트입니다. ")


class Answer(BaseModel):
    message: str = Field(description="사용자의 질문에 대응하는 AI 챗봇의 답변 텍스트입니다. ")

    def to_dict(self):
        return {
            "message": self.message,
        }
