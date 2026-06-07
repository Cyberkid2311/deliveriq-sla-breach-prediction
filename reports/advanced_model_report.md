# Advanced Model Report

## Business Summary

The selected final model is `LightGBM Classifier`.
The selection prioritizes catching SLA breaches, then precision, F1-score, PR-AUC, and ROC-AUC.
The best default-threshold recall model is `Random Forest`.
The best default-threshold precision-recall balance by F1 is `XGBoost Classifier`.

Advanced models were implemented with LightGBM and XGBoost as requested, then compared against the three Day 4 baselines on the same held-out test split.

## Model Comparison

| Model | Accuracy | Precision Class 1 | Recall Class 1 | F1 Class 1 | ROC-AUC | PR-AUC | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.6823 | 0.1477 | 0.6115 | 0.2379 | 0.7045 | 0.1825 | Baseline |
| Decision Tree | 0.6532 | 0.1297 | 0.5738 | 0.2116 | 0.6690 | 0.1657 | Baseline |
| Random Forest | 0.6039 | 0.1242 | 0.6415 | 0.2081 | 0.6664 | 0.1630 | Baseline |
| LightGBM Classifier | 0.7259 | 0.1619 | 0.5700 | 0.2522 | 0.7145 | 0.2042 | Advanced final model candidate |
| XGBoost Classifier | 0.7458 | 0.1667 | 0.5335 | 0.2540 | 0.7131 | 0.2064 | Advanced optional comparison model |

## Recall-First Threshold Review

| Model | Threshold | Precision Class 1 | Recall Class 1 | F1 Class 1 | False Positives | False Negatives |
| --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.2500 | 0.1005 | 0.8914 | 0.1806 | 12488 | 170 |
| Decision Tree | 0.3000 | 0.1015 | 0.8428 | 0.1811 | 11679 | 246 |
| Random Forest | 0.4500 | 0.1012 | 0.8371 | 0.1806 | 11632 | 255 |
| LightGBM Classifier | 0.2500 | 0.1000 | 0.9137 | 0.1803 | 12865 | 135 |
| XGBoost Classifier | 0.2500 | 0.1016 | 0.8971 | 0.1826 | 12412 | 161 |

## Final Model Selection

- Final model: `LightGBM Classifier`
- Saved artifact: `models/final_model.pkl`
- Default operating threshold: 0.25
- Recall class 1: 0.9137
- Precision class 1: 0.1000
- F1 class 1: 0.1803
- PR-AUC: 0.2042

## Risk Bucket Logic

| Probability Range | Risk Bucket | Action |
| ---: | --- | --- |
| 0.00-0.30 | Low | No action |
| >0.30-0.60 | Medium | Monitor |
| >0.60-0.80 | High | Prioritize |
| >0.80-1.00 | Critical | Immediate intervention |

## Implemented Model Lineup

- Baseline 1: Logistic Regression
- Baseline 2: Decision Tree
- Baseline 3: Random Forest
- Advanced 1: LightGBM Classifier
- Advanced 2: XGBoost Classifier
