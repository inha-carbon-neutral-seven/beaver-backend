from typing import List
from pydantic import BaseModel, Field


class RecommendationOutput(BaseModel):
    recommendations: List[str] = Field(
        description="한국어로 된, 물음표로 끝나는 존댓말 양식을 가지는 질문",
        min_items=3,
    )

    def to_dict(self):
        return {
            "recommendations": self.recommendations,
        }
