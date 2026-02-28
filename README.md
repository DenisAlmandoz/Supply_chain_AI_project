# End-to-End Supply Chain AI Solution

This repository contains a practical, layered starter architecture for a supply-chain AI product.

## Layers implemented

- **Data Layer** (`backend/app/layers/data_layer.py`): synthetic demand dataset creation and feature generation.
- **MLOps Layer** (`backend/app/layers/mlops_layer.py`): model training, validation (MAE), and active model registry.
- **LLM Layer** (`backend/app/layers/llm_layer.py`): guardrailed Q&A that only responds to supply-chain topics.
- **Infra Layer** (`backend/app/layers/infra_layer.py`): future API integration surface (ERP/WMS/supplier portals).
- **Tooling Layer** (`backend/app/layers/tooling_layer.py`): tracing metadata hooks for observability.
- **React Layer** (`frontend/index.html`): browser UI for Q&A and demand prediction.
- **API Orchestration Layer** (`backend/app/main.py`): FastAPI endpoints that compose all layers.

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then open `http://localhost:8000`.

## Endpoints

- `GET /health` — returns layer status and active model version.
- `POST /predict` — predicts next-week demand from simple supply features.
- `POST /qa` — answers only supply-chain questions with guardrails.

## Future extension ideas

- replace synthetic data with warehouse/ERP ingestion pipelines
- add feature store + model registry (MLflow)
- add vector DB and real LLM API integration
- connect infra layer adapters to real external APIs
- add auth and tenant-level controls
