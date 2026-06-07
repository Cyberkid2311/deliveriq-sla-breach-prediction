# Model Evaluation Report

## Summary

Five classification models were evaluated for SLA breach prediction:

- Logistic Regression
- Decision Tree
- Random Forest
- LightGBM Classifier
- XGBoost Classifier

All models were evaluated on the same stratified 20% holdout test set. The target class `1` represents an SLA breach.

## Selection Priority

The final model is not selected by accuracy alone. The project priority order is:

1. Recall for class `1`
2. Precision for class `1`
3. F1-score for class `1`
4. PR-AUC
5. ROC-AUC
6. Accuracy as a secondary metric

Recall is the primary metric because the business goal is to catch as many delayed orders as possible before they breach SLA.

## Default Threshold Metrics

| Model | Accuracy | Precision Class 1 | Recall Class 1 | F1 Class 1 | ROC-AUC | PR-AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.6823 | 0.1477 | 0.6115 | 0.2379 | 0.7045 | 0.1825 |
| Decision Tree | 0.6532 | 0.1297 | 0.5738 | 0.2116 | 0.6690 | 0.1657 |
| Random Forest | 0.6039 | 0.1242 | 0.6415 | 0.2081 | 0.6664 | 0.1630 |
| LightGBM Classifier | 0.7259 | 0.1619 | 0.5700 | 0.2522 | 0.7145 | 0.2042 |
| XGBoost Classifier | 0.7458 | 0.1667 | 0.5335 | 0.2540 | 0.7131 | 0.2064 |

## Recall-First Threshold Metrics

| Model | Threshold | Precision Class 1 | Recall Class 1 | F1 Class 1 | False Positives | False Negatives | True Positives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.25 | 0.1005 | 0.8914 | 0.1806 | 12,488 | 170 | 1,395 |
| Decision Tree | 0.30 | 0.1015 | 0.8428 | 0.1811 | 11,679 | 246 | 1,319 |
| Random Forest | 0.45 | 0.1012 | 0.8371 | 0.1806 | 11,632 | 255 | 1,310 |
| LightGBM Classifier | 0.25 | 0.1000 | 0.9137 | 0.1803 | 12,865 | 135 | 1,430 |
| XGBoost Classifier | 0.25 | 0.1016 | 0.8971 | 0.1826 | 12,412 | 161 | 1,404 |

## Final Model

The selected final model is `LightGBM Classifier` at threshold `0.25`.

It catches the highest share of actual SLA breaches among the evaluated models:

- Recall class 1: 0.9137
- False negatives: 135
- True positives: 1,430
- Precision class 1: 0.1000
- False positives: 12,865

## Interpretation

LightGBM is best for the project objective because it identifies the most SLA breaches under the recall-first selection rule. The tradeoff is that it produces many false alerts. This is acceptable for a recall-first early warning system only if operations has enough capacity to review flagged orders.

## Overfitting And Stability

The Day 4 review compared train and test behavior for the baseline models. For the final advanced workflow, the same held-out test set is used consistently and model selection is based on test metrics plus threshold behavior. A future improvement is to add cross-validation or time-based validation to better assess stability across periods and routes.
