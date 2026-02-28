from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    PredictionRequest,
    PredictionResponse,
    QARequest,
    QAResponse,
    HealthResponse,
)
from .layers.data_layer import DataLayer
from .layers.mlops_layer import MLOpsLayer
from .layers.llm_layer import LLMLayer
from .layers.infra_layer import InfraLayer
from .layers.tooling_layer import ToolingLayer

app = FastAPI(title="Supply Chain AI Solution", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Layer composition
_data = DataLayer()
_mlops = MLOpsLayer()
_llm = LLMLayer()
_infra = InfraLayer()
_tooling = ToolingLayer()
_model = _mlops.train_and_register(_data.generate_training_data())


@app.get("/", include_in_schema=False)
def ui() -> FileResponse:
    frontend_file = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
    return FileResponse(frontend_file)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        layers={
            "data_layer": "ready",
            "mlops_layer": f"ready:{_model.version}",
            "llm_layer": "ready",
            "infra_layer": str(_infra.get_status()),
            "tooling_layer": "ready",
        },
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    artifact = _mlops.get_active_model()
    row = [[
        payload.inventory_level,
        payload.lead_time_days,
        payload.historical_weekly_demand,
        payload.supplier_reliability_score,
    ]]
    pred = float(artifact.model.predict(row)[0])
    _tooling.build_trace("predict")
    return PredictionResponse(predicted_next_week_demand=round(pred, 2), model_version=artifact.version)


@app.post("/qa", response_model=QAResponse)
def qa(payload: QARequest) -> QAResponse:
    answer, references = _llm.answer(payload.question)
    _tooling.build_trace("qa")
    return QAResponse(answer=answer, references=references)
