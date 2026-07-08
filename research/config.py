from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "job_salary_prediction_dataset.csv"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
MODELS_DIR = ROOT_DIR / "models"
MODEL_PATH = MODELS_DIR / "salary_model.joblib"
METADATA_PATH = MODELS_DIR / "model_metadata.json"

TARGET = "salary"
RANDOM_STATE = 42

CATEGORICAL_COLUMNS = [
    "job_title",
    "education_level",
    "industry",
    "company_size",
    "location",
    "remote_work",
]
NUMERIC_COLUMNS = ["experience_years", "skills_count", "certifications"]
FEATURE_COLUMNS = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS


def ensure_output_dirs() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(exist_ok=True)
