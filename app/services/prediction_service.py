from app.models.retail_model import get_model
from app.schemas.prediction import (
    PredictionInput, PredictionOutput,
    BatchPredictionInput, BatchPredictionOutput
)


def predict_single(data: PredictionInput) -> PredictionOutput:
    model = get_model()
    result = model.predict_single(
        year=data.year,
        month=data.month,
        item_type=data.item_type,
        retail_transfers=data.retail_transfers,
        warehouse_sales=data.warehouse_sales,
    )
    return PredictionOutput(
        predicted_retail_sales=result,
        model_used=model.metadata["model_name"],
        input_received=data.model_dump(),
    )


def predict_batch(data: BatchPredictionInput) -> BatchPredictionOutput:
    model = get_model()
    items = [item.model_dump() for item in data.items]
    predictions = model.predict_batch(items)
    return BatchPredictionOutput(
        predictions=predictions,
        count=len(predictions),
        model_used=model.metadata["model_name"],
    )
