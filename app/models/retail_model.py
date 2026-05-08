import joblib
import json
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parents[2] / "models"
FEATURE_COLS = ["YEAR", "MONTH", "ITEM TYPE", "RETAIL TRANSFERS", "WAREHOUSE SALES"]


class RetailDemandModel:
    def __init__(self):
        self.model = joblib.load(MODEL_DIR / "best_model.pkl")
        self.scaler = joblib.load(MODEL_DIR / "scaler.pkl")
        self.item_type_encoder = joblib.load(MODEL_DIR / "item_type_encoder.pkl")

        with open(MODEL_DIR / "metadata.json") as f:
            self.metadata = json.load(f)

    def encode_item_type(self, item_type: str) -> int:
        classes = list(self.item_type_encoder.classes_)
        item_type_upper = item_type.upper()
        if item_type_upper not in classes:
            raise ValueError(
                f"item_type '{item_type}' tidak dikenal. "
                f"Pilihan valid: {[c for c in classes if c and c != 'nan']}"
            )
        return int(self.item_type_encoder.transform([item_type_upper])[0])

    def _to_df(self, rows: list) -> pd.DataFrame:
        return pd.DataFrame(rows, columns=FEATURE_COLS)

    def predict_single(self, year: int, month: int, item_type: str,
                       retail_transfers: float, warehouse_sales: float) -> float:
        item_type_encoded = self.encode_item_type(item_type)
        X = self._to_df([[year, month, item_type_encoded, retail_transfers, warehouse_sales]])
        prediction = self.model.predict(X)[0]
        return max(0.0, round(float(prediction), 4))

    def predict_batch(self, items: list[dict]) -> list[float]:
        rows = []
        for item in items:
            item_type_encoded = self.encode_item_type(item["item_type"])
            rows.append([
                item["year"], item["month"], item_type_encoded,
                item["retail_transfers"], item["warehouse_sales"]
            ])
        X = self._to_df(rows)
        preds = self.model.predict(X)
        return [max(0.0, round(float(p), 4)) for p in preds]


# Singleton — loaded once on startup
_model_instance: RetailDemandModel | None = None


def get_model() -> RetailDemandModel:
    global _model_instance
    if _model_instance is None:
        _model_instance = RetailDemandModel()
    return _model_instance
