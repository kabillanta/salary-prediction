from __future__ import annotations

import os
import json
import warnings
from functools import lru_cache

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from google import genai
from google.genai import types

from research.config import FEATURE_COLUMNS, MODEL_PATH, METADATA_PATH

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


@lru_cache(maxsize=1)
def get_allowed_categories():
    if METADATA_PATH.exists():
        with open(METADATA_PATH) as f:
            data = json.load(f)
            return data.get("input_categories", {})
    return {}


app = FastAPI(title="Salary Prediction API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict_gemini", response_model=SalaryPrediction)
def predict_gemini(payload: SalaryInput) -> SalaryPrediction:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not set. Cannot use Gemini.")
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)

    system_prompt = f"""You are an expert compensation analyst and salary predictor.
A user has provided their professional profile containing custom or niche job titles/industries.
Your task is to estimate their current market salary in USD based on this profile.

Rules:
1. Output ONLY a valid, structured JSON object in this exact format: {{"predicted_salary": 150000.00}}
2. Do not include markdown formatting like ```json or any other text.
3. Be as accurate as possible based on standard tech/industry compensation data for the provided location and experience level.
"""

    prompt = json.dumps(payload.model_dump())
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
            ),
        )
        prediction_data = json.loads(response.text)
        return SalaryPrediction(**prediction_data)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        raise HTTPException(status_code=500, detail="Failed to get prediction from Gemini API.")


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
