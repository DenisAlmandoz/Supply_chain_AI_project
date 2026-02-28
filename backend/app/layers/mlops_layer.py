from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


@dataclass
class ModelArtifact:
    model: LinearRegression
    version: str
    training_mae: float


class MLOpsLayer:
    """Tiny local model lifecycle layer (train, validate, register)."""

    def __init__(self) -> None:
        self._artifact: ModelArtifact | None = None

    def train_and_register(self, df) -> ModelArtifact:
        features = [
            "inventory_level",
            "lead_time_days",
            "historical_weekly_demand",
            "supplier_reliability_score",
        ]
        x = df[features]
        y = df["next_week_demand"]

        model = LinearRegression()
        model.fit(x, y)
        preds = model.predict(x)
        mae = float(mean_absolute_error(y, preds))

        version = f"v1-mae-{mae:.2f}"
        self._artifact = ModelArtifact(model=model, version=version, training_mae=mae)
        return self._artifact

    def get_active_model(self) -> ModelArtifact:
        if not self._artifact:
            raise RuntimeError("No active model registered.")
        return self._artifact
