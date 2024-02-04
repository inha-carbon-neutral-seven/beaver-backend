from typing import List, Union
from enum import Enum
from pydantic import BaseModel, Field


class ChartType(str, Enum):
    BAR = "bar"
    PIE = "pie"


class Series(BaseModel):
    name: str
    data: List[Union[int, float]]


class ChartOutput(BaseModel):
    series: List[Series] = Field(
        description="""List of series points for the chart,
        each containing a name, type, and data points."""
    )
    labels: List[str] = Field(
        description="List of labels for the chart, providing context to the displayed data."
    )
    title: str = Field(description="The title representing the visualization of the chart.")
    type: ChartType = Field(
        description="""The type of chart to be displayed on the dashboard.
        It determines the overall layout and the way data is represented in the chart.
        "bar" type will represent data in rectangular bars, helpful for comparing quantities across categories.
        "pie" type will represent data in sectors of a circle, 
        ideal for showing the proportion of parts against the whole."""
    )

    def to_dict(self):
        return {
            "series": self.series,
            "labels": self.labels,
            "title": self.title,
            "type": self.type,
        }
