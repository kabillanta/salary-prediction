from __future__ import annotations

import warnings
from functools import lru_cache

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from research.config import FEATURE_COLUMNS, MODEL_PATH

warnings.filterwarnings("ignore", message="X does not have valid feature names")


class SalaryInput(BaseModel):
    job_title: str = Field(..., examples=["Data Scientist"])
    experience_years: int = Field(..., ge=0, examples=[5])
    education_level: str = Field(..., examples=["Master"])
    skills_count: int = Field(..., ge=0, examples=[10])
    industry: str = Field(..., examples=["Technology"])
    company_size: str = Field(..., examples=["Large"])
    location: str = Field(..., examples=["USA"])
    remote_work: str = Field(..., examples=["Hybrid"])
    certifications: int = Field(..., ge=0, examples=[2])


class SalaryPrediction(BaseModel):
    predicted_salary: float


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model artifact not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


app = FastAPI(title="Salary Prediction API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=SalaryPrediction)
def predict_salary(payload: SalaryInput) -> SalaryPrediction:
    try:
        model = load_model()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503, detail="Train the model first with `pixi run train`."
        ) from exc

    row = pd.DataFrame([payload.model_dump()])[FEATURE_COLUMNS]
    prediction = float(model.predict(row)[0])
    return SalaryPrediction(predicted_salary=round(prediction, 2))
