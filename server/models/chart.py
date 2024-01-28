from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class ChartType(str, Enum):
    LINE = "line"
    AREA = "area"
    BAR = "bar"
    COLUMN = "column"
    BOXPLOT = "boxPlot"
    RANGEBAR = "rangeBar"
    RANGEAREA = "rangeArea"
    HEATMAP = "heatmap"
    TREEMAP = "treemap"
    RADAR = "radar"
    RADIALBAR = "radialbar"
    PIE = "pie"
    DONUT = "donut"


class Series(BaseModel):
    name: str
    type: ChartType
    data: List[int]


class ChartOutput(BaseModel):
    series: List[Series] = Field(
        description="""List of series points for the chart,
        each containing a name, type, and data points."""
    )
    labels: List[str] = Field(
        description="List of labels for the chart, providing context to the displayed data."
    )
    title: str = Field(description="The title representing the visualization of the chart.")

    def to_dict(self):
        return {
            "series": self.series,
            "labels": self.labels,
            "title": self.title,
        }
