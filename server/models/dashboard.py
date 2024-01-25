from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class DashboardType(str, Enum):
    LINE = "LINE"
    PIE = "PIE"
    BAR = "BAR"


class DashboardOutput(BaseModel):
    type: DashboardType = Field(
        description="""
        The type of data to be displayed on the dashboard. 
        Choose from DashboardType.LINE, DashboardType.PIE, DashboardType.BAR."""
    )
    title: str = Field(description="The title representing the visualization of the dashboard.")
    labels: List[str] = Field(
        description="List of labels for the dashboard, providing context to the displayed data."
    )
    data: List[int] = Field(
        description="""
        List of data points for the dashboard, 
        representing the actual values to be visualized."""
    )

    def to_dict(self):
        return {
            "title": self.title,
            "type": self.type,
            "labels": self.labels,
            "data": self.data,
        }
