from __future__ import annotations

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.model_selection import train_test_split

from research.config import FIGURES_DIR, MODEL_PATH, RANDOM_STATE, REPORTS_DIR, ensure_output_dirs
from research.data_utils import load_dataset, split_features_target


def transformed_feature_names(preprocess_pipeline) -> list[str]:
    return preprocess_pipeline.named_steps["preprocessor"].get_feature_names_out().tolist()


def main() -> None:
    ensure_output_dirs()
    pipeline = joblib.load(MODEL_PATH)
    df = load_dataset()
    x, y = split_features_target(df)
    _, x_test, _, _ = train_test_split(x, y, test_size=0.2, random_state=RANDOM_STATE)

    sample = x_test.sample(n=min(1500, len(x_test)), random_state=RANDOM_STATE)
    background = x_test.sample(n=min(500, len(x_test)), random_state=RANDOM_STATE + 1)

    preprocess = pipeline.named_steps["preprocess"]
    model = pipeline.named_steps["model"]
    x_sample = preprocess.transform(sample)
    feature_names = transformed_feature_names(preprocess)

    try:
        explainer = shap.TreeExplainer(model)
        values = explainer.shap_values(x_sample)
        if isinstance(values, list):
            values = values[0]
        base_value = explainer.expected_value
        if isinstance(base_value, np.ndarray):
            base_value = float(base_value.ravel()[0])
        shap_values = shap.Explanation(
            values=values,
            base_values=np.full(x_sample.shape[0], base_value),
            data=x_sample,
            feature_names=feature_names,
        )
    except Exception:
        x_background = preprocess.transform(background)
        masker = shap.maskers.Independent(x_background, max_samples=100)
        explainer = shap.Explainer(model.predict, masker, feature_names=feature_names)
        shap_values = explainer(x_sample[:300])

    importance = pd.DataFrame(
        {
            "feature": feature_names,
            "mean_abs_shap": np.abs(shap_values.values).mean(axis=0),
        }
    ).sort_values("mean_abs_shap", ascending=False)
    importance.to_csv(REPORTS_DIR / "shap_feature_importance.csv", index=False)

    shap.plots.beeswarm(shap_values, max_display=20, show=False)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "shap_summary.png", dpi=160, bbox_inches="tight")
    plt.close()

    shap.plots.bar(shap_values, max_display=20, show=False)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "shap_bar.png", dpi=160, bbox_inches="tight")
    plt.close()

    print("SHAP outputs saved to reports/.")


if __name__ == "__main__":
    main()
