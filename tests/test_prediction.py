from fastapi.testclient import TestClient
from src.main import app

valid_payload = {
    "age": 45,
    "gender": "Male",
    "tenure_months": 24,
    "monthly_charges": 79.5,
    "total_charges": 1900.0,
    "contract_type": "Month-to-month",
    "payment_method": "Electronic check",
    "paperless_billing": "Yes",
    "num_support_tickets": 1,
    "num_logins_last_month": 12,
    "feature_usage_score": 65.5,
    "late_payments": 0,
    "partner": "Yes",
    "dependents": "No",
    "internet_service": "Fiber optic",
    "online_security": "No",
    "online_backup": "Yes",
    "device_protection": "No",
    "tech_support": "No",
    "streaming_tv": "Yes",
    "streaming_movies": "Yes"
}

def test_predict_valid():
    with TestClient(app) as client:
        response = client.post("/predict", json=valid_payload)
        assert response.status_code == 200
        assert "prediction" in response.json()
        assert "probability" in response.json()


def test_predict_invalid():
    with TestClient(app) as client:
        response = client.post("/predict", json={"age": 45})
        assert response.status_code == 422

def test_batch_predict_valid():
    batch_payload = {
        "customers": [valid_payload, valid_payload]
    }

    with TestClient(app) as client:
        response = client.post("/batch-predict", json=batch_payload)
        assert response.status_code == 200
        assert "results" in response.json()
        assert len(response.json()["results"]) == 2