from fastapi import FastAPI, HTTPException
from src.models import CustomerInput
import pickle
import pandas as pd
from src.models import CustomerInput, BatchCustomerInput
import os

app = FastAPI(title="Customer Churn Prediction API")

MODEL_PATH = os.getenv("MODEL_PATH", "models/churn_model.pkl")
PREPROCESS_PATH = os.getenv("PREPROCESS_PATH", "models/preprocessing.pkl")

model = None
preprocessing = None


@app.on_event("startup")
def load_artifacts():
    global model, preprocessing

    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        with open(PREPROCESS_PATH, "rb") as f:
            preprocessing = pickle.load(f)

    except Exception as e:
        print(f"Error loading artifacts: {e}")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/readiness")
def readiness():
    if model is None or preprocessing is None:
        raise HTTPException(status_code=503, detail="Model not ready")
    return {"status": "ready"}

@app.post("/predict")
def predict(customer: CustomerInput):
    if model is None or preprocessing is None:
        raise HTTPException(status_code=503, detail="Model not ready")

    input_dict = customer.dict()
    input_df = pd.DataFrame([input_dict])

    for col in preprocessing["feature_columns"]:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[preprocessing["feature_columns"]]

    for col in preprocessing["categorical_cols"]:
        le = preprocessing["label_encoders"][col]
        input_df[col] = le.transform(input_df[col])

    input_df[preprocessing["numerical_cols"]] = preprocessing["scaler"].transform(
        input_df[preprocessing["numerical_cols"]]
    )

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }

@app.post("/batch-predict")
def batch_predict(batch: BatchCustomerInput):
    if model is None or preprocessing is None:
        raise HTTPException(status_code=503, detail="Model not ready")

    results = []

    for customer in batch.customers:
        input_dict = customer.dict()
        input_df = pd.DataFrame([input_dict])

        for col in preprocessing["feature_columns"]:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[preprocessing["feature_columns"]]

        for col in preprocessing["categorical_cols"]:
            le = preprocessing["label_encoders"][col]
            input_df[col] = le.transform(input_df[col])

        input_df[preprocessing["numerical_cols"]] = preprocessing["scaler"].transform(
            input_df[preprocessing["numerical_cols"]]
        )

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        results.append(
            {
                "prediction": int(prediction),
                "probability": float(probability)
            }
        )

    return {"results": results}