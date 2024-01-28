from typing import List
from pydantic import BaseModel, Field


class RecommendationOutput(BaseModel):
    recommendations: List[str] = Field(
        description="Recommended questions for users to ask",
        min_items=3,
    )

    def to_dict(self):
        return {
            "recommendations": self.recommendations,
        }
