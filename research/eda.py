from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from research.config import CATEGORICAL_COLUMNS, FIGURES_DIR, NUMERIC_COLUMNS, REPORTS_DIR, TARGET, ensure_output_dirs
from research.data_utils import dataframe_to_markdown, load_dataset, write_markdown


def save_bar(series: pd.Series, title: str, xlabel: str, ylabel: str, path: str, figsize=(10, 5)) -> None:
    ax = series.plot(kind="bar", figsize=figsize, color="#4c78a8")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / path, dpi=160)
    plt.close()


def save_eda_plots(df: pd.DataFrame) -> None:
    ax = df[TARGET].plot(kind="hist", bins=50, figsize=(9, 5), color="#59a14f", edgecolor="white")
    ax.set_title("Salary Distribution")
    ax.set_xlabel("Salary")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "salary_distribution.png", dpi=160)
    plt.close()

    df[NUMERIC_COLUMNS].hist(bins=30, figsize=(10, 7), color="#f28e2b", edgecolor="white")
    plt.suptitle("Numeric Feature Distributions")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "numeric_distributions.png", dpi=160)
    plt.close()

    save_bar(
        df.groupby("job_title")[TARGET].mean().sort_values(ascending=False),
        "Average Salary by Job Title",
        "Job title",
        "Average salary",
        "salary_by_job_title.png",
        figsize=(11, 5),
    )
    save_bar(
        df.groupby("location")[TARGET].mean().sort_values(ascending=False),
        "Average Salary by Location",
        "Location",
        "Average salary",
        "salary_by_location.png",
    )
    save_bar(
        df.groupby("education_level")[TARGET].mean().sort_values(ascending=False),
        "Average Salary by Education Level",
        "Education level",
        "Average salary",
        "salary_by_education.png",
    )
    save_bar(
        df.groupby("experience_years")[TARGET].mean(),
        "Average Salary by Experience Years",
        "Experience years",
        "Average salary",
        "salary_by_experience.png",
        figsize=(11, 5),
    )

    corr = df[NUMERIC_COLUMNS + [TARGET]].corr()
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)), labels=corr.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(corr.index)), labels=corr.index)
    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="black")
    fig.colorbar(im, ax=ax)
    ax.set_title("Numeric Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "correlation_heatmap.png", dpi=160)
    plt.close()


def build_summary(df: pd.DataFrame) -> list[str]:
    missing = df.isna().sum()
    salary_summary = df[TARGET].describe()
    top_locations = df.groupby("location")[TARGET].mean().sort_values(ascending=False).head(5)
    top_jobs = df.groupby("job_title")[TARGET].mean().sort_values(ascending=False).head(5)
    categorical_counts = [f"- `{col}`: {df[col].nunique()} unique values" for col in CATEGORICAL_COLUMNS]

    return [
        "# Exploratory Data Analysis Summary",
        (
            "## Dataset Structure\n"
            f"- Rows: {df.shape[0]:,}\n"
            f"- Columns: {df.shape[1]}\n"
            f"- Target column: `{TARGET}`\n"
            f"- Duplicate rows: {df.duplicated().sum():,}"
        ),
        "## Data Types\n" + dataframe_to_markdown(df.dtypes.astype(str).to_frame("dtype")),
        "## Missing Values\n" + dataframe_to_markdown(missing.to_frame("missing_count")),
        "## Categorical Cardinality\n" + "\n".join(categorical_counts),
        "## Salary Distribution\n" + dataframe_to_markdown(salary_summary.to_frame("salary")),
        "## Numeric Feature Summary\n" + dataframe_to_markdown(df[NUMERIC_COLUMNS].describe()),
        "## Highest Average Salaries by Location\n" + dataframe_to_markdown(top_locations.round(0).to_frame("average_salary")),
        "## Highest Average Salaries by Job Title\n" + dataframe_to_markdown(top_jobs.round(0).to_frame("average_salary")),
        (
            "## Main EDA Findings\n"
            "- The dataset is already clean: no missing values and no duplicate rows were found.\n"
            "- Salary varies strongly by location, with USA, Canada, UK, and Germany above most other locations.\n"
            "- AI Engineer and Machine Learning Engineer roles have the highest average salaries.\n"
            "- Experience, skills, and certifications are numeric predictors and should be kept for modeling.\n"
            "- Categorical variables have manageable cardinality, so one-hot encoding is appropriate."
        ),
        (
            "## Generated Figures\n"
            "- `reports/figures/salary_distribution.png`\n"
            "- `reports/figures/numeric_distributions.png`\n"
            "- `reports/figures/salary_by_job_title.png`\n"
            "- `reports/figures/salary_by_location.png`\n"
            "- `reports/figures/salary_by_education.png`\n"
            "- `reports/figures/salary_by_experience.png`\n"
            "- `reports/figures/correlation_heatmap.png`"
        ),
    ]


def main() -> None:
    ensure_output_dirs()
    df = load_dataset()
    save_eda_plots(df)
    write_markdown(REPORTS_DIR / "eda_summary.md", build_summary(df))
    print("EDA outputs saved to reports/.")


if __name__ == "__main__":
    main()
