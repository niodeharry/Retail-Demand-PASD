# Retail Demand Prediction API

Aplikasi prediksi permintaan produk retail menggunakan Machine Learning.

**Kelompok:** Orang-orang Sukses | **Kelas:** DS-48-01 | **Telkom University 2026**

---

## Struktur Project

```
retail-demand-api/
├── app/
│   ├── main.py              # Entry point FastAPI
│   ├── models/              # Model loader & wrapper
│   ├── schemas/             # Pydantic input/output validation
│   ├── services/            # Business logic
│   └── routers/             # Endpoint definitions
├── models/                  # Saved .pkl artifacts
├── notebooks/               # EDA & model training notebook
├── data/                    # Dataset
├── tests/                   # Unit tests (pytest)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Setup & Menjalankan API

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train model (jika belum ada .pkl)

Jalankan notebook `notebooks/retail_demand_pipeline.ipynb` dari awal sampai selesai.

### 3. Jalankan API lokal

```bash
uvicorn app.main:app --reload --port 8000
```

API berjalan di `http://localhost:8000`. Swagger UI tersedia di `http://localhost:8000/docs`.

### 4. Jalankan dengan Docker

```bash
# Build image
docker build -t retail-demand-api .

# Jalankan container
docker compose up -d

# Cek status
docker compose logs -f

# Hentikan
docker compose down
```

### 5. Mode development (hot-reload)

```bash
docker compose --profile dev up
```

## Menjalankan Tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Informasi API |
| GET | `/health` | Status & metrik model |
| POST | `/api/v1/predict` | Prediksi satu produk |
| POST | `/api/v1/predict/batch` | Prediksi hingga 50 produk |

## Contoh Request

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2024,
    "month": 6,
    "item_type": "WINE",
    "retail_transfers": 10.5,
    "warehouse_sales": 25.0
  }'
```

Respons:
```json
{
  "predicted_retail_sales": 8.3241,
  "model_used": "Gradient Boosting",
  "input_received": {...}
}
```

## Model Performance

| Model | MAE | RMSE | R² |
|-------|-----|------|----|
| Gradient Boosting | 1.6928 | 6.4537 | 0.9501 |
| Linear Regression | 1.6927 | 6.6322 | 0.9473 |
| Random Forest | 1.7454 | 7.4055 | 0.9343 |
| Decision Tree | 2.1208 | 9.2362 | 0.8977 |

Model terbaik: **Gradient Boosting** (RMSE terendah, R² = 0.95)

## Item Types yang Didukung

`BEER`, `DUNNAGE`, `KEGS`, `LIQUOR`, `NON-ALCOHOL`, `REF`, `STR_SUPPLIES`, `WINE`
