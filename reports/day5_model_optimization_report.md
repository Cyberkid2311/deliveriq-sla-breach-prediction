# Day 5 Model Optimization Report

## Dataset

- Source: `data\processed\feature_dataset.csv`
- Training rows: 77,176
- Test rows: 19,294
- Target: `sla_breached`
- Train SLA breach rate: 8.11%
- Test SLA breach rate: 8.11%
- Test split: stratified 20% holdout with random_state=42

## Optimization Approach

- Added model-safe delivery estimate, route, and order intensity features.
- Trained sklearn-only optimized candidates.
- Evaluated probability thresholds from 0.05 to 0.95.
- Selected thresholds using recall first after basic precision and false-positive guardrails.

## Default Threshold Model Comparison

| Model | Accuracy | Precision Class 1 | Recall Class 1 | F1 Class 1 | PR-AUC | ROC-AUC |
| --- | --- | --- | --- | --- | --- | --- |
| Optimized Logistic Regression | 0.7433 | 0.1676 | 0.5457 | 0.2564 | 0.1899 | 0.7084 |
| Optimized Random Forest | 0.6325 | 0.1339 | 0.6460 | 0.2219 | 0.1640 | 0.6786 |
| HistGradientBoosting | 0.9189 | 0.6000 | 0.0019 | 0.0038 | 0.2078 | 0.7200 |

## Selected Recall-First Thresholds

| Model | Threshold | Precision Class 1 | Recall Class 1 | F1 Class 1 | PR-AUC | ROC-AUC | False Positives | False Negatives | True Positives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Optimized Logistic Regression | 0.2000 | 0.1020 | 0.8843 | 0.1829 | 0.1899 | 0.7084 | 12188 | 181 | 1384 |
| Optimized Random Forest | 0.5000 | 0.1339 | 0.6460 | 0.2219 | 0.1640 | 0.6786 | 6537 | 554 | 1011 |
| HistGradientBoosting | 0.0500 | 0.1088 | 0.8754 | 0.1935 | 0.2078 | 0.7200 | 11224 | 195 | 1370 |

## Recommended Operational Model

- Model: `Optimized Logistic Regression`
- Threshold: 0.20
- Recall class 1: 0.8843
- Precision class 1: 0.1020
- False negatives: 181
- False positives: 12188
