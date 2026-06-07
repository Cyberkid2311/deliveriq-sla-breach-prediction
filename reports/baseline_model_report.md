# Baseline Model Report

## Dataset

- Source: `data/processed/feature_dataset.csv`
- Training rows: 77,176
- Test rows: 19,294
- Target: `sla_breached`
- Train SLA breach rate: 8.11%
- Test SLA breach rate: 8.11%
- Test split: stratified 20% holdout with random_state=42

## Feature Handling

- `X` uses only the approved model features from `docs/feature_list_v1.md`.
- ID columns and leakage columns are excluded from model input.
- Numeric features use median imputation and standard scaling.
- Categorical features use `Unknown` imputation and one-hot encoding with unknown-category handling.
- `purchase_day_of_week` is treated as a categorical feature.

## Saved Model Artifacts

- `models/baseline_logistic_regression.pkl`
- `models/baseline_decision_tree.pkl`
- `models/baseline_random_forest.pkl`

## Model Comparison

| Model | Accuracy | Precision Class 1 | Recall Class 1 | F1 Class 1 | ROC-AUC | PR-AUC |
| --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.6822 | 0.1477 | 0.6115 | 0.2379 | 0.7045 | 0.1825 |
| Decision Tree | 0.6532 | 0.1297 | 0.5738 | 0.2116 | 0.6690 | 0.1657 |
| Random Forest | 0.6039 | 0.1242 | 0.6415 | 0.2081 | 0.6664 | 0.1630 |

Best baseline by class-1 recall, then PR-AUC, then class-1 precision: `Random Forest`.

## Confusion Matrices

### Logistic Regression

| Actual / Predicted | Predicted 0 | Predicted 1 |
| --- | ---: | ---: |
| Actual 0 | 12206 | 5523 |
| Actual 1 | 608 | 957 |

### Decision Tree

| Actual / Predicted | Predicted 0 | Predicted 1 |
| --- | ---: | ---: |
| Actual 0 | 11704 | 6025 |
| Actual 1 | 667 | 898 |

### Random Forest

| Actual / Predicted | Predicted 0 | Predicted 1 |
| --- | ---: | ---: |
| Actual 0 | 10648 | 7081 |
| Actual 1 | 561 | 1004 |

## Classification Reports

### Logistic Regression

```text
precision    recall  f1-score   support

     on_time       0.95      0.69      0.80     17729
sla_breached       0.15      0.61      0.24      1565

    accuracy                           0.68     19294
   macro avg       0.55      0.65      0.52     19294
weighted avg       0.89      0.68      0.75     19294
```

### Decision Tree

```text
precision    recall  f1-score   support

     on_time       0.95      0.66      0.78     17729
sla_breached       0.13      0.57      0.21      1565

    accuracy                           0.65     19294
   macro avg       0.54      0.62      0.49     19294
weighted avg       0.88      0.65      0.73     19294
```

### Random Forest

```text
precision    recall  f1-score   support

     on_time       0.95      0.60      0.74     17729
sla_breached       0.12      0.64      0.21      1565

    accuracy                           0.60     19294
   macro avg       0.54      0.62      0.47     19294
weighted avg       0.88      0.60      0.69     19294
```
