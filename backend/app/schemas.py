from pydantic import BaseModel, Field
from typing import Dict, List


class PredictionRequest(BaseModel):
    inventory_level: float = Field(..., ge=0)
    lead_time_days: float = Field(..., ge=0)
    historical_weekly_demand: float = Field(..., ge=0)
    supplier_reliability_score: float = Field(..., ge=0, le=1)


class PredictionResponse(BaseModel):
    predicted_next_week_demand: float
    model_version: str


class QARequest(BaseModel):
    question: str = Field(..., min_length=3)


class QAResponse(BaseModel):
    answer: str
    references: List[str]


class HealthResponse(BaseModel):
    status: str
    layers: Dict[str, str]
