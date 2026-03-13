# Customer Churn Prediction – MLOps Use Case

## Overview
This project implements an end-to-end MLOps workflow for customer churn prediction. The solution covers:
- model training with saved artifacts,
- FastAPI model serving,
- Docker containerization,
- Docker Compose deployment,
- automated API testing,
- basic CI with GitHub Actions.

The main goal of this project is not only to train a model, but to show how the model can be packaged, validated, and served as a small production-style prediction service.

## Architecture
`customer_churn_dataset.csv` -> `train_model.py` -> `models/` artifacts -> `src/main.py` FastAPI app -> Docker image -> Docker Compose deployment

## Repository Structure
```text
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI workflow: install, test, Docker build
├── config/
│   └── settings.md                # Configuration notes
├── models/
│   ├── churn_model.pkl            # Trained Random Forest model
│   ├── preprocessing.pkl          # Saved encoders, scaler, feature metadata
│   └── metrics.pkl                # Saved evaluation metrics
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app and inference endpoints
│   └── models.py                  # Pydantic request schemas
├── tests/
│   ├── __init__.py
│   ├── test_api.py                # Health/readiness and endpoint tests
│   └── test_prediction.py         # Prediction request validation tests
├── .gitignore
├── CICD_APPROACH.md               # CI/CD design notes
├── Dockerfile                     # Docker image definition
├── README.md                      # Project documentation
├── customer_churn_dataset.csv     # Training dataset
├── docker-compose.yml             # Local deployment configuration
├── requirements.txt               # Runtime dependencies
├── requirements-dev.txt           # Development/testing dependencies
└── train_model.py                 # Model training pipeline
```

## Prerequisites
- Python 3.11+
- Docker Desktop
- Git

## 1. Setup and Model Training
Create a virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Train the model:

```bash
python train_model.py
```

This script:
- loads the churn dataset,
- encodes categorical variables,
- scales numerical variables,
- splits the data into train and test sets,
- trains a Random Forest Classifier,
- evaluates the model,
- saves all deployment artifacts.

Generated artifacts:
- `models/churn_model.pkl`
- `models/preprocessing.pkl`
- `models/metrics.pkl`

### Model Details
- **Algorithm:** Random Forest Classifier
- **Categorical preprocessing:** Label encoding
- **Numerical preprocessing:** Standard scaling
- **Saved preprocessing metadata:** label encoders, scaler, categorical columns, numerical columns, feature column order

### Model Evaluation Results
Add the real values from `models/metrics.pkl` after training:

- Accuracy: `[add value]`
- Precision: `[add value]`
- Recall: `[add value]`
- F1-score: `[add value]`

## 2. Run Application Locally
After training, start the FastAPI service:

```bash
uvicorn src.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

Note: model artifacts must exist in the `models/` directory before starting the API.

## 3. Run with Docker
Build the Docker image:

```bash
docker build -t churn-api .
```

Run the container:

```bash
docker run -p 8000:8000 churn-api
```

This step validates that the application works as a standalone container.

## 4. Run with Docker Compose
Start the service:

```bash
docker compose up --build
```

Stop the service:

```bash
docker compose down
```

### Why Docker Compose?
Docker Compose was chosen instead of Kubernetes because it is simpler for local deployment and still demonstrates deployment configuration, environment management, and health monitoring in a reproducible way.

## API Endpoints
### `GET /health`
Checks if the API process is running.

Example response:
```json
{
  "status": "ok"
}
```

### `GET /readiness`
Checks if model artifacts were loaded and the service is ready to serve predictions.

Possible responses:
```json
{
  "status": "ready"
}
```

or, if artifacts are missing:

```json
{
  "status": "not ready"
}
```

### `POST /predict`
Returns a prediction for a single customer.

Example request:
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

Example response:
```json
{
  "prediction": 0,
  "churn_probability": 0.31
}
```

### `POST /batch-predict`
Returns predictions for multiple customers in one request.

Example request:
```json
{
  "customers": [
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
  ]
}
```

## 5. Testing
Run automated tests with:

```bash
pytest -v
```

Current tests cover:
- `/health` endpoint
- `/readiness` endpoint
- valid single prediction requests
- invalid request validation
- batch prediction requests

## 6. CI/CD
This project includes a GitHub Actions workflow in `.github/workflows/ci.yml`.

Current CI pipeline:
- runs on push to `main`,
- runs on pull requests to `main`,
- installs Python dependencies,
- runs `pytest`,
- builds the Docker image to validate the container setup.

`CICD_APPROACH.md` describes how this basic CI flow could be extended toward fuller CD later, such as image tagging, registry push, and environment deployment.

## 7. Deployment Approach
The application is packaged with Docker and deployed locally with Docker Compose. This setup demonstrates the core deployment flow required by the task:
- reproducible runtime environment,
- service startup from configuration,
- health monitoring,
- readiness checks,
- automated validation through tests and CI.

For a larger production environment, the same container image could later be deployed to Kubernetes or another orchestrated platform.

## 8. Evidence of Working Solution
Add screenshots or links here to satisfy the deliverables more clearly:
- Swagger UI (`/docs`)
- successful `/health` response
- successful `/readiness` response
- sample `/predict` response
- `docker compose up --build` running successfully
- passing GitHub Actions workflow

## 9. Future Improvements
- add stronger model-side unit tests for preprocessing and artifacts,
- add structured logging and centralized exception handling,
- add security scanning and linting to CI,
- add image publishing and deployment automation,
- add staging environment before production deployment.
