from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class ChartType(str, Enum):
    BAR = "bar"
    PIE = "pie"


class Series(BaseModel):
    name: str
    data: List[int]


class ChartOutput(BaseModel):
    cid: int = Field(description="The unique integer identifier for the chart.")
    series: List[Series] = Field(
        description="""List of series points for the chart,
        each containing a name, type, and data points."""
    )
    labels: List[str] = Field(
        description="List of labels for the chart, providing context to the displayed data."
    )
    title: str = Field(description="The title representing the visualization of the chart.")
    type: ChartType = Field(
        description="""
        The type of data to be displayed on the dashboard. 
        Choose a chart type between ChartType.PIE, ChartType.BAR."""
    )

    def to_dict(self):
        return {
            "cid": self.cid,
            "series": self.series,
            "labels": self.labels,
            "title": self.title,
            "type": self.type,
        }
