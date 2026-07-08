# Salary Prediction Project

Install Pixi first: https://pixi.sh/latest/

## Structure

```text
backend/    FastAPI prediction service
frontend/   Frontend application workspace
research/   EDA, training, and SHAP scripts
data/       Dataset
models/     Generated model artifacts
reports/    Report summaries and figures
```

## Start

1. Install dependencies:

```bash
pixi install
```

2. Generate reports, model, and SHAP outputs:

```bash
pixi run all
```

3. Start the backend API:

```bash
pixi run api
```

4. Open API docs:

```text
http://127.0.0.1:8000/docs
```

## Commands

```bash
pixi run eda
pixi run train
pixi run shap
pixi run api
```
