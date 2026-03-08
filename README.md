# Customer Churn Prediction – MLOps Use Case

## Overview

This project implements an end-to-end MLOps pipeline for deploying a Customer Churn Prediction model.

The solution includes:

- Model training pipeline
- FastAPI inference service
- Docker containerization
- Docker Compose deployment
- Automated testing with pytest
- Health and readiness monitoring

---

## Project Structure

```
├── src/                    # FastAPI source code
│   ├── main.py
│   └── models.py
├── models/                 # Trained model artifacts
<<<<<<< HEAD
├── config/                 #configuration
├── tests/                  # Automated tests
├── train_model.py          # Model training script
├── customer_churn_dataset.csv
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Multi-container deployment
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.11+
- Docker Desktop
- Git

---

## 1️⃣ Model Training

Create virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Train the model:

```bash
python train_model.py
```

Generated artifacts:

- `models/churn_model.pkl`
- `models/preprocessing.pkl`
- `models/metrics.pkl`

---

## 2️⃣ Run Application Locally

Start FastAPI server:

```bash
uvicorn src.main:app --reload
```

Open Swagger UI:

```
http://localhost:8000/docs
```

---

## 3️⃣ Run with Docker

Build Docker image:

```bash
docker build -t churn-api .
```

Run container:

```bash
docker run -p 8000:8000 churn-api
```

---

## 4️⃣ Run with Docker Compose

Start services:

```bash
docker compose up --build
```

Stop services:

```bash
docker compose down
```

---

## API Endpoints

### Health Check
GET `/health`

### Readiness Check
GET `/readiness`

### Predict
POST `/predict`

Example request body:

```json
{
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
```

---

## 5️⃣ Running Tests

```bash
pytest -v
```

All tests should pass successfully.

---

## Deployment Approach

The application is containerized using Docker and deployed locally using Docker Compose.  
Health and readiness endpoints ensure the service is production-ready.

This structure supports future CI/CD automation and scalable deployment.

---

## Model Details

- Algorithm: Random Forest Classifier
- Preprocessing:
  - Label encoding for categorical variables
  - Standard scaling for numerical features
- Metrics stored in:
  - `models/metrics.pkl`

---


