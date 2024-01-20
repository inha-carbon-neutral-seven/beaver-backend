from typing import List
from pydantic import BaseModel, Field


class RecommendationOutput(BaseModel):
    status: bool = True
    recommendations: List[str] = Field(description="Recommended questions for users to ask")

    def to_dict(self):
        return {
            "status": self.status,
            "recommendations": self.recommendations,
        }
