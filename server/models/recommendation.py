from typing import List
from pydantic import BaseModel, Field


class RecommendationOutput(BaseModel):
    recommendations: List[str] = Field(
        description="Recommended questions for users to ask",
        min_items=3,
    )

    class Config:
        schema_extra = {
            "example": {
                "recommendations": [
                    "2023 하반기에 주목해야 할 소매업계 이슈는 무엇인가요?",
                    "디지털, 비용관리, 생성형 AI, PB, 불확실성 대응 체력을 키우기 위한 대응책은 무엇인가요?",
                    "소매업계 데이터를 통해 어떤 정보를 얻을 수 있나요?",
                ]
            }
        }

    def to_dict(self):
        return {
            "recommendations": self.recommendations,
        }
