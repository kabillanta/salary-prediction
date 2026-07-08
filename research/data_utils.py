from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from research.config import CATEGORICAL_COLUMNS, DATA_PATH, FEATURE_COLUMNS, NUMERIC_COLUMNS, TARGET


def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    return df[FEATURE_COLUMNS].copy(), df[TARGET].copy()


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["has_certification"] = (result["certifications"] > 0).astype(int)
    result["skills_per_experience"] = result["skills_count"] / (result["experience_years"] + 1)
    result["experience_bucket"] = pd.cut(
        result["experience_years"],
        bins=[-1, 2, 5, 10, 15, 100],
        labels=["entry", "junior", "mid", "senior", "expert"],
    ).astype(str)
    return result


def build_preprocessor(use_engineered_features: bool, scale_numeric: bool = False) -> Pipeline:
    categorical_columns = list(CATEGORICAL_COLUMNS)
    numeric_columns = list(NUMERIC_COLUMNS)

    steps = []
    if use_engineered_features:
        steps.append(("features", FunctionTransformer(add_engineered_features, validate=False)))
        categorical_columns.append("experience_bucket")
        numeric_columns.extend(["has_certification", "skills_per_experience"])

    numeric_transformer = StandardScaler() if scale_numeric else "passthrough"
    column_transformer = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_columns),
            ("numeric", numeric_transformer, numeric_columns),
        ],
        verbose_feature_names_out=False,
    )
    steps.append(("preprocessor", column_transformer))
    return Pipeline(steps)


def get_pipeline_feature_names(pipeline: Pipeline) -> list[str]:
    preprocessor = pipeline.named_steps["preprocessor"]
    return preprocessor.get_feature_names_out().tolist()


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_markdown(path: Path, sections: list[str]) -> None:
    path.write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    table = df.reset_index()
    columns = [str(col) for col in table.columns]
    rows = [[str(value) for value in row] for row in table.to_numpy()]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header, separator] + body)
