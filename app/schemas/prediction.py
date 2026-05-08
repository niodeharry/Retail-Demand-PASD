from pydantic import BaseModel, Field, ConfigDict


class PredictionInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "year": 2024,
                "month": 6,
                "item_type": "WINE",
                "retail_transfers": 10.5,
                "warehouse_sales": 25.0,
            }
        }
    )

    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    item_type: str
    retail_transfers: float = Field(..., ge=0.0)
    warehouse_sales: float = Field(..., ge=0.0)


class PredictionOutput(BaseModel):
    predicted_retail_sales: float
    model_used: str
    input_received: dict


class BatchPredictionInput(BaseModel):
    items: list[PredictionInput] = Field(..., max_length=50)


class BatchPredictionOutput(BaseModel):
    predictions: list[float]
    count: int
    model_used: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    metrics: dict
