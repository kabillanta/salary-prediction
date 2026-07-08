# Salary Prediction Project Summary

## Modeling Approach
- Categorical variables were one-hot encoded because each categorical column has low cardinality.
- Numeric variables were kept as numeric inputs. Ridge regression used scaling; tree models did not require scaling.
- Missing-value imputation was not used because the dataset contains no missing values.
- Outlier removal was not applied because high and low salaries are plausible target values for this prediction problem.

## Feature Engineering
- `has_certification` marks whether a candidate has at least one certification.
- `skills_per_experience` captures skill density relative to experience.
- `experience_bucket` groups years of experience into entry, junior, mid, senior, and expert levels.
- In the LightGBM comparison, engineered features improved performance based on test RMSE.

## Model Comparison
| index | model | train_mae | test_mae | train_rmse | test_rmse | train_r2 | test_r2 | fit_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | LightGBM Engineered | 3975.5455 | 4135.6257 | 4984.3539 | 5185.473 | 0.9823 | 0.9807 | 3.9272 |
| 1 | LightGBM Base | 3979.7011 | 4144.3846 | 4994.2509 | 5193.1371 | 0.9822 | 0.9806 | 2.9353 |
| 2 | Ridge Regression | 5470.716 | 5436.4557 | 7166.3363 | 7125.833 | 0.9634 | 0.9635 | 0.7443 |
| 3 | Random Forest | 6509.1154 | 7141.6296 | 8411.7417 | 9059.6385 | 0.9495 | 0.9409 | 16.1273 |
| 4 | Baseline Mean | 29807.7242 | 29694.6403 | 37439.5602 | 37280.8806 | 0.0 | -0.0 | 0.4497 |

## Feature Set Comparison
| index | model | train_mae | test_mae | train_rmse | test_rmse | train_r2 | test_r2 | fit_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | engineered_features | 3975.5455 | 4135.6257 | 4984.3539 | 5185.473 | 0.9823 | 0.9807 | 3.516 |
| 1 | base_features | 3979.7011 | 4144.3846 | 4994.2509 | 5193.1371 | 0.9822 | 0.9806 | 2.8931 |

## Final Model Decision
- Selected model: LightGBM Engineered
- Test MAE: 4135.63
- Test RMSE: 5185.47
- Test R2: 0.9807
- The final model was selected by lowest test RMSE while also checking MAE and R2.

## Reproduction Commands
```bash
pixi run eda
pixi run train
pixi run shap
pixi run api
```
