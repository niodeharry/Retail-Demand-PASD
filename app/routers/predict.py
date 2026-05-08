from fastapi import APIRouter, HTTPException
from app.schemas.prediction import (
    PredictionInput, PredictionOutput,
    BatchPredictionInput, BatchPredictionOutput
)
from app.services import prediction_service

router = APIRouter(prefix="/api/v1", tags=["Prediction"])


@router.post("/predict", response_model=PredictionOutput)
async def predict(data: PredictionInput) -> PredictionOutput:
    """
    Prediksi retail sales untuk satu produk berdasarkan fitur input.
    """
    try:
        return prediction_service.predict_single(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/predict/batch", response_model=BatchPredictionOutput)
async def predict_batch(data: BatchPredictionInput) -> BatchPredictionOutput:
    """
    Prediksi retail sales untuk hingga 50 produk sekaligus.
    """
    try:
        return prediction_service.predict_batch(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")
