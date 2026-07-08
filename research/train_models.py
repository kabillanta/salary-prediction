from __future__ import annotations

import time
import warnings

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from research.config import (
    CATEGORICAL_COLUMNS,
    FEATURE_COLUMNS,
    FIGURES_DIR,
    METADATA_PATH,
    MODEL_PATH,
    RANDOM_STATE,
    REPORTS_DIR,
    TARGET,
    ensure_output_dirs,
)
from research.data_utils import build_preprocessor, dataframe_to_markdown, load_dataset, split_features_target, write_json, write_markdown


def rmse(y_true: pd.Series, y_pred: np.ndarray) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def evaluate_model(name: str, pipeline: Pipeline, x_train, x_test, y_train, y_test) -> dict:
    start = time.perf_counter()
    pipeline.fit(x_train, y_train)
    train_pred = pipeline.predict(x_train)
    test_pred = pipeline.predict(x_test)
    return {
        "model": name,
        "train_mae": mean_absolute_error(y_train, train_pred),
        "test_mae": mean_absolute_error(y_test, test_pred),
        "train_rmse": rmse(y_train, train_pred),
        "test_rmse": rmse(y_test, test_pred),
        "train_r2": r2_score(y_train, train_pred),
        "test_r2": r2_score(y_test, test_pred),
        "fit_seconds": time.perf_counter() - start,
    }


def make_pipeline(model, use_engineered_features: bool, scale_numeric: bool = False) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocess", build_preprocessor(use_engineered_features, scale_numeric=scale_numeric)),
            ("model", model),
        ]
    )


def model_candidates() -> list[tuple[str, Pipeline]]:
    return [
        ("Baseline Mean", make_pipeline(DummyRegressor(strategy="mean"), False)),
        ("Ridge Regression", make_pipeline(Ridge(alpha=1.0), True, scale_numeric=True)),
        (
            "Random Forest",
            make_pipeline(
                RandomForestRegressor(
                    n_estimators=60,
                    max_depth=16,
                    min_samples_leaf=5,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
                True,
            ),
        ),
        (
            "LightGBM Base",
            make_pipeline(
                LGBMRegressor(
                    n_estimators=500,
                    learning_rate=0.06,
                    num_leaves=63,
                    subsample=0.9,
                    colsample_bytree=0.9,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                    verbosity=-1,
                ),
                False,
            ),
        ),
        (
            "LightGBM Engineered",
            make_pipeline(
                LGBMRegressor(
                    n_estimators=500,
                    learning_rate=0.06,
                    num_leaves=63,
                    subsample=0.9,
                    colsample_bytree=0.9,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                    verbosity=-1,
                ),
                True,
            ),
        ),
    ]


def compare_feature_sets(x_train, x_test, y_train, y_test) -> pd.DataFrame:
    rows = []
    for label, engineered in [("base_features", False), ("engineered_features", True)]:
        pipeline = make_pipeline(
            LGBMRegressor(
                n_estimators=500,
                learning_rate=0.06,
                num_leaves=63,
                subsample=0.9,
                colsample_bytree=0.9,
                random_state=RANDOM_STATE,
                n_jobs=-1,
                verbosity=-1,
            ),
            engineered,
        )
        result = evaluate_model(label, pipeline, x_train, x_test, y_train, y_test)
        rows.append(result)
    return pd.DataFrame(rows).sort_values("test_rmse").reset_index(drop=True)


def save_diagnostic_plots(y_test: pd.Series, predictions: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y_test, predictions, s=8, alpha=0.25, color="#4c78a8")
    limits = [min(y_test.min(), predictions.min()), max(y_test.max(), predictions.max())]
    ax.plot(limits, limits, color="#e15759", linewidth=2)
    ax.set_title("Actual vs Predicted Salary")
    ax.set_xlabel("Actual salary")
    ax.set_ylabel("Predicted salary")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "actual_vs_predicted.png", dpi=160)
    plt.close()

    residuals = y_test - predictions
    ax = pd.Series(residuals).plot(kind="hist", bins=50, figsize=(8, 5), color="#f28e2b", edgecolor="white")
    ax.set_title("Residual Distribution")
    ax.set_xlabel("Actual - predicted salary")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "residuals.png", dpi=160)
    plt.close()


def build_project_summary(model_results: pd.DataFrame, feature_results: pd.DataFrame, final_model_name: str) -> list[str]:
    best = model_results.iloc[0]
    feature_best = feature_results.iloc[0]
    feature_note = "improved" if feature_best["model"] == "engineered_features" else "did not improve"
    return [
        "# Salary Prediction Project Summary",
        (
            "## Modeling Approach\n"
            "- Categorical variables were one-hot encoded because each categorical column has low cardinality.\n"
            "- Numeric variables were kept as numeric inputs. Ridge regression used scaling; tree models did not require scaling.\n"
            "- Missing-value imputation was not used because the dataset contains no missing values.\n"
            "- Outlier removal was not applied because high and low salaries are plausible target values for this prediction problem."
        ),
        (
            "## Feature Engineering\n"
            "- `has_certification` marks whether a candidate has at least one certification.\n"
            "- `skills_per_experience` captures skill density relative to experience.\n"
            "- `experience_bucket` groups years of experience into entry, junior, mid, senior, and expert levels.\n"
            f"- In the LightGBM comparison, engineered features {feature_note} performance based on test RMSE."
        ),
        "## Model Comparison\n" + dataframe_to_markdown(model_results.round(4)),
        "## Feature Set Comparison\n" + dataframe_to_markdown(feature_results.round(4)),
        (
            "## Final Model Decision\n"
            f"- Selected model: {final_model_name}\n"
            f"- Test MAE: {best['test_mae']:.2f}\n"
            f"- Test RMSE: {best['test_rmse']:.2f}\n"
            f"- Test R2: {best['test_r2']:.4f}\n"
            "- The final model was selected by lowest test RMSE while also checking MAE and R2."
        ),
        (
            "## Reproduction Commands\n"
            "```bash\n"
            "pixi run eda\n"
            "pixi run train\n"
            "pixi run shap\n"
            "pixi run api\n"
            "```"
        ),
    ]


def main() -> None:
    warnings.filterwarnings("ignore", message="X does not have valid feature names")
    ensure_output_dirs()
    df = load_dataset()
    x, y = split_features_target(df)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=RANDOM_STATE)

    feature_results = compare_feature_sets(x_train, x_test, y_train, y_test)
    feature_results.to_csv(REPORTS_DIR / "feature_engineering_comparison.csv", index=False)

    rows = []
    fitted_models = {}
    for name, pipeline in model_candidates():
        rows.append(evaluate_model(name, pipeline, x_train, x_test, y_train, y_test))
        fitted_models[name] = pipeline

    model_results = pd.DataFrame(rows).sort_values("test_rmse").reset_index(drop=True)
    model_results.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)

    final_model_name = str(model_results.loc[0, "model"])
    final_pipeline = fitted_models[final_model_name]
    test_predictions = final_pipeline.predict(x_test)
    save_diagnostic_plots(y_test, test_predictions)

    joblib.dump(final_pipeline, MODEL_PATH)
    write_json(
        METADATA_PATH,
        {
            "final_model": final_model_name,
            "target": TARGET,
            "feature_columns": FEATURE_COLUMNS,
            "categorical_columns": CATEGORICAL_COLUMNS,
            "random_state": RANDOM_STATE,
            "test_size": 0.2,
            "metrics": model_results.loc[0].to_dict(),
            "input_categories": {col: sorted(df[col].unique().tolist()) for col in CATEGORICAL_COLUMNS},
        },
    )
    write_markdown(REPORTS_DIR / "project_summary.md", build_project_summary(model_results, feature_results, final_model_name))
    print("Training outputs saved to models/ and reports/.")


if __name__ == "__main__":
    main()
