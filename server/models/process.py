from typing import List, Optional, Union

from enum import Enum
from pydantic import BaseModel

from .recap import RecapOutput
from .chart import ChartOutput


class ProcessType(str, Enum):
    RECAP = "recap"
    RECOMMENDATION = "recommendation"
    CHART = "chart"


class ProcessInput(BaseModel):
    type: ProcessType


class ProcessOutput(BaseModel):
    status: bool
    type: Optional[ProcessType]
    output: Optional[Union[RecapOutput, List[str], List[ChartOutput]]]
