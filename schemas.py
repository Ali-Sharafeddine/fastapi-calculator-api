from pydantic import BaseModel
from typing import Literal

class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: Literal["add", "subtract", "divide"]