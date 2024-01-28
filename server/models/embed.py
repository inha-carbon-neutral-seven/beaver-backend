from typing import List, Optional
from pydantic import BaseModel
from .dashboard import ChartOutput
from .recap import RecapOutput


class EmbedOutput(BaseModel):
    status: bool
    recap: Optional[RecapOutput]
    recommendations: Optional[List[str]]  # RecommendationOutput
    chart: Optional[List[ChartOutput]]
