from fastapi import FastAPI
from datetime import datetime
from app.routers import predict
from app.models.retail_model import get_model
from app.schemas.prediction import HealthResponse

app = FastAPI(
    title="Retail Demand Prediction API",
    description=(
        "API prediksi permintaan produk retail menggunakan Machine Learning. "
        "Kelompok: Orang-orang Sukses | DS-48-01 | Telkom University 2026"
    ),
    version="1.0.0",
)

app.include_router(predict.router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Retail Demand Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    model = get_model()
    return HealthResponse(
        status="ok",
        model_loaded=True,
        model_name=model.metadata["model_name"],
        metrics=model.metadata["metrics"],
    )
