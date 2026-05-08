import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ── 1. Health check ──
def test_health_returns_200():
    r = client.get("/health")
    assert r.status_code == 200


def test_health_response_structure():
    r = client.get("/health")
    data = r.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True
    assert "model_name" in data
    assert "metrics" in data


# ── 2. Root endpoint ──
def test_root_returns_200():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


# ── 3. Single predict — happy path ──
def test_predict_wine():
    r = client.post("/api/v1/predict", json={
        "year": 2024,
        "month": 6,
        "item_type": "WINE",
        "retail_transfers": 10.0,
        "warehouse_sales": 20.0,
    })
    assert r.status_code == 200
    data = r.json()
    assert "predicted_retail_sales" in data
    assert data["predicted_retail_sales"] >= 0


def test_predict_beer():
    r = client.post("/api/v1/predict", json={
        "year": 2023,
        "month": 12,
        "item_type": "BEER",
        "retail_transfers": 5.0,
        "warehouse_sales": 15.0,
    })
    assert r.status_code == 200
    assert r.json()["predicted_retail_sales"] >= 0


def test_predict_liquor():
    r = client.post("/api/v1/predict", json={
        "year": 2024,
        "month": 1,
        "item_type": "LIQUOR",
        "retail_transfers": 8.0,
        "warehouse_sales": 30.0,
    })
    assert r.status_code == 200


# ── 4. Single predict — unhappy path ──
def test_predict_invalid_item_type():
    r = client.post("/api/v1/predict", json={
        "year": 2024,
        "month": 6,
        "item_type": "BARANG_TIDAK_ADA",
        "retail_transfers": 10.0,
        "warehouse_sales": 20.0,
    })
    assert r.status_code == 422


def test_predict_missing_field():
    r = client.post("/api/v1/predict", json={
        "year": 2024,
        "month": 6,
        "item_type": "WINE",
        # retail_transfers dan warehouse_sales tidak ada
    })
    assert r.status_code == 422


def test_predict_invalid_month():
    r = client.post("/api/v1/predict", json={
        "year": 2024,
        "month": 13,  # bulan tidak valid
        "item_type": "WINE",
        "retail_transfers": 10.0,
        "warehouse_sales": 20.0,
    })
    assert r.status_code == 422


def test_predict_empty_body():
    r = client.post("/api/v1/predict", json={})
    assert r.status_code == 422


# ── 5. Batch predict ──
def test_predict_batch_returns_200():
    r = client.post("/api/v1/predict/batch", json={
        "items": [
            {"year": 2024, "month": 1, "item_type": "WINE",
             "retail_transfers": 5.0, "warehouse_sales": 10.0},
            {"year": 2024, "month": 2, "item_type": "BEER",
             "retail_transfers": 3.0, "warehouse_sales": 8.0},
            {"year": 2024, "month": 3, "item_type": "LIQUOR",
             "retail_transfers": 7.0, "warehouse_sales": 20.0},
        ]
    })
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 3
    assert len(data["predictions"]) == 3


def test_predict_batch_count_matches():
    items = [
        {"year": 2024, "month": i, "item_type": "WINE",
         "retail_transfers": float(i), "warehouse_sales": float(i * 2)}
        for i in range(1, 6)
    ]
    r = client.post("/api/v1/predict/batch", json={"items": items})
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == len(items)
    assert len(data["predictions"]) == len(items)
