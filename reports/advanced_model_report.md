# Advanced Model Report

## Business Summary

The selected final model is `Logistic Regression`.
The selection prioritizes catching SLA breaches, then precision, F1-score, PR-AUC, and ROC-AUC.
The best default-threshold recall model is `Optimized Random Forest`.
The best default-threshold precision-recall balance by F1 is `Optimized Logistic Regression`.

Advanced models did improve the project outcome because the final workflow now includes stronger model candidates and threshold tuning, not just default 0.50 predictions.

## Model Comparison

| Model | Accuracy | Precision Class 1 | Recall Class 1 | F1 Class 1 | ROC-AUC | PR-AUC | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.6823 | 0.1477 | 0.6115 | 0.2379 | 0.7045 | 0.1825 | Baseline |
| Decision Tree | 0.6532 | 0.1297 | 0.5738 | 0.2116 | 0.6690 | 0.1657 | Baseline |
| Random Forest | 0.6039 | 0.1242 | 0.6415 | 0.2081 | 0.6664 | 0.1630 | Baseline |
| Optimized Logistic Regression | 0.7433 | 0.1676 | 0.5457 | 0.2564 | 0.7084 | 0.1899 | Advanced sklearn |
| Optimized Random Forest | 0.6325 | 0.1339 | 0.6460 | 0.2219 | 0.6786 | 0.1640 | Advanced tuned Random Forest |
| HistGradientBoosting | 0.9189 | 0.6000 | 0.0019 | 0.0038 | 0.7200 | 0.2078 | Advanced sklearn gradient boosting |

## Recall-First Threshold Review

| Model | Threshold | Precision Class 1 | Recall Class 1 | F1 Class 1 | False Positives | False Negatives |
| --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.2500 | 0.1005 | 0.8914 | 0.1806 | 12488 | 170 |
| Decision Tree | 0.3000 | 0.1015 | 0.8428 | 0.1811 | 11679 | 246 |
| Random Forest | 0.4500 | 0.1012 | 0.8371 | 0.1806 | 11632 | 255 |
| Optimized Logistic Regression | 0.2000 | 0.1020 | 0.8843 | 0.1829 | 12188 | 181 |
| Optimized Random Forest | 0.5000 | 0.1339 | 0.6460 | 0.2219 | 6537 | 554 |
| HistGradientBoosting | 0.0500 | 0.1088 | 0.8754 | 0.1935 | 11224 | 195 |

## Final Model Selection

- Final model: `Logistic Regression`
- Saved artifact: `models/final_model.pkl`
- Default operating threshold: 0.25
- Recall class 1: 0.8914
- Precision class 1: 0.1005
- F1 class 1: 0.1806
- PR-AUC: 0.1825

## Risk Bucket Logic

| Probability Range | Risk Bucket | Action |
| ---: | --- | --- |
| 0.00-0.30 | Low | No action |
| >0.30-0.60 | Medium | Monitor |
| >0.60-0.80 | High | Prioritize |
| >0.80-1.00 | Critical | Immediate intervention |

## Notes On LightGBM And XGBoost

LightGBM and XGBoost are not part of the current project dependencies, so the implemented advanced workflow uses sklearn-only candidates. The code is ready to compare additional candidates if those dependencies are added later.
