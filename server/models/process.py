from typing import List, Optional, Union

from enum import Enum
from pydantic import BaseModel, Field

from .recap import RecapOutput
from .chart import ChartOutput


class ProcessType(str, Enum):
    EMBED = "embed"
    RECAP = "recap"
    RECOMMENDATION = "recommendation"
    CHART = "chart"


class ProcessInput(BaseModel):
    type: ProcessType


class ProcessOutput(BaseModel):
    status: bool = Field(False)
    type: Optional[ProcessType] = Field(None)
    output: Optional[Union[RecapOutput, List[str], List[ChartOutput]]] = Field(None)
