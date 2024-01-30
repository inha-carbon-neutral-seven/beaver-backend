from typing import List
from pydantic import BaseModel, Field


class RecommendationOutput(BaseModel):
    recommendations: List[str] = Field(
        description="This is a list of questions that will best answer your questions.",
        min_items=3,
    )

    def to_dict(self):
        return {
            "recommendations": self.recommendations,
        }
