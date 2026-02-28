import numpy as np
import pandas as pd


class DataLayer:
    """Data acquisition and feature generation layer."""

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed

    def generate_training_data(self, n_samples: int = 500) -> pd.DataFrame:
        rng = np.random.default_rng(self.seed)
        inventory = rng.uniform(100, 4000, n_samples)
        lead_time = rng.uniform(1, 45, n_samples)
        historical_demand = rng.uniform(50, 1200, n_samples)
        reliability = rng.uniform(0.6, 1.0, n_samples)
        seasonal = rng.normal(0, 40, n_samples)

        target = (
            0.05 * inventory
            + 2.5 * lead_time
            + 0.75 * historical_demand
            - 350 * reliability
            + seasonal
        )

        df = pd.DataFrame(
            {
                "inventory_level": inventory,
                "lead_time_days": lead_time,
                "historical_weekly_demand": historical_demand,
                "supplier_reliability_score": reliability,
                "next_week_demand": target.clip(min=10),
            }
        )
        return df
