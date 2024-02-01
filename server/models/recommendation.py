from typing import List
from pydantic import BaseModel, Field


class RecommendationOutput(BaseModel):
    recommendations: List[str] = Field(
        description="물음표로 끝나며 한국어 존댓말 양식을 가지는 질문. 반드시 질문문 형식를 지켜야 합니다. ",
        min_items=3,
    )

    def to_dict(self):
        return {
            "recommendations": self.recommendations,
        }
