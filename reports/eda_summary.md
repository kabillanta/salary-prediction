# Exploratory Data Analysis Summary

## Dataset Structure
- Rows: 250,000
- Columns: 10
- Target column: `salary`
- Duplicate rows: 0

## Data Types
| index | dtype |
| --- | --- |
| job_title | str |
| experience_years | int64 |
| education_level | str |
| skills_count | int64 |
| industry | str |
| company_size | str |
| location | str |
| remote_work | str |
| certifications | int64 |
| salary | int64 |

## Missing Values
| index | missing_count |
| --- | --- |
| job_title | 0 |
| experience_years | 0 |
| education_level | 0 |
| skills_count | 0 |
| industry | 0 |
| company_size | 0 |
| location | 0 |
| remote_work | 0 |
| certifications | 0 |
| salary | 0 |

## Categorical Cardinality
- `job_title`: 12 unique values
- `education_level`: 5 unique values
- `industry`: 10 unique values
- `company_size`: 5 unique values
- `location`: 10 unique values
- `remote_work`: 3 unique values

## Salary Distribution
| index | salary |
| --- | --- |
| count | 250000.0 |
| mean | 145718.080524 |
| std | 37407.952729244156 |
| min | 31867.0 |
| 25% | 119358.0 |
| 50% | 143453.0 |
| 75% | 169492.0 |
| max | 333046.0 |

## Numeric Feature Summary
| index | experience_years | skills_count | certifications |
| --- | --- | --- | --- |
| count | 250000.0 | 250000.0 | 250000.0 |
| mean | 10.005408 | 9.997812 | 2.491928 |
| std | 6.0606024186662095 | 5.47928821135129 | 1.7064754586720443 |
| min | 0.0 | 1.0 | 0.0 |
| 25% | 5.0 | 5.0 | 1.0 |
| 50% | 10.0 | 10.0 | 2.0 |
| 75% | 15.0 | 15.0 | 4.0 |
| max | 20.0 | 19.0 | 5.0 |

## Highest Average Salaries by Location
| location | average_salary |
| --- | --- |
| USA | 181716.0 |
| Canada | 167391.0 |
| UK | 160075.0 |
| Germany | 153376.0 |
| Remote | 139443.0 |

## Highest Average Salaries by Job Title
| job_title | average_salary |
| --- | --- |
| AI Engineer | 173498.0 |
| Machine Learning Engineer | 163023.0 |
| Product Manager | 157595.0 |
| Cloud Engineer | 152103.0 |
| DevOps Engineer | 149959.0 |

## Main EDA Findings
- The dataset is already clean: no missing values and no duplicate rows were found.
- Salary varies strongly by location, with USA, Canada, UK, and Germany above most other locations.
- AI Engineer and Machine Learning Engineer roles have the highest average salaries.
- Experience, skills, and certifications are numeric predictors and should be kept for modeling.
- Categorical variables have manageable cardinality, so one-hot encoding is appropriate.

## Generated Figures
- `reports/figures/salary_distribution.png`
- `reports/figures/numeric_distributions.png`
- `reports/figures/salary_by_job_title.png`
- `reports/figures/salary_by_location.png`
- `reports/figures/salary_by_education.png`
- `reports/figures/salary_by_experience.png`
- `reports/figures/correlation_heatmap.png`
