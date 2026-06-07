# Day 5 - Model Optimization Notes

## Summary

The Day 5 advanced modeling workflow now implements the requested five-model lineup:

- Logistic Regression
- Decision Tree
- Random Forest
- LightGBM Classifier
- XGBoost Classifier

All models are evaluated on the same stratified train/test split and selected using the project priority order: recall for the SLA breach class, then precision, F1-score, PR-AUC, and ROC-AUC.

## Advanced Model Implementation

LightGBM and XGBoost are implemented as pipeline-based models with the same approved pre-delivery feature set. Both use class imbalance handling through model-specific weighting.

The final selected model is `LightGBM Classifier` at threshold `0.25`.

## Model Comparison

| Model | Accuracy | Precision Class 1 | Recall Class 1 | F1 Class 1 | ROC-AUC | PR-AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.6823 | 0.1477 | 0.6115 | 0.2379 | 0.7045 | 0.1825 |
| Decision Tree | 0.6532 | 0.1297 | 0.5738 | 0.2116 | 0.6690 | 0.1657 |
| Random Forest | 0.6039 | 0.1242 | 0.6415 | 0.2081 | 0.6664 | 0.1630 |
| LightGBM Classifier | 0.7259 | 0.1619 | 0.5700 | 0.2522 | 0.7145 | 0.2042 |
| XGBoost Classifier | 0.7458 | 0.1667 | 0.5335 | 0.2540 | 0.7131 | 0.2064 |

## Recall-First Threshold Results

| Model | Threshold | Recall | Precision | F1 | False Positives | False Negatives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.25 | 0.8914 | 0.1005 | 0.1806 | 12,488 | 170 |
| Decision Tree | 0.30 | 0.8428 | 0.1015 | 0.1811 | 11,679 | 246 |
| Random Forest | 0.45 | 0.8371 | 0.1012 | 0.1806 | 11,632 | 255 |
| LightGBM Classifier | 0.25 | 0.9137 | 0.1000 | 0.1803 | 12,865 | 135 |
| XGBoost Classifier | 0.25 | 0.8971 | 0.1016 | 0.1826 | 12,412 | 161 |

## Business Interpretation

LightGBM is selected because it catches the most SLA breaches under the recall-first threshold strategy. It reduces false negatives from the Day 4 best baseline Random Forest count of 561 to 135.

The tradeoff is a high false-positive count, so the threshold should be reviewed against operations capacity before production use.

## Deliverables

- `src/models/train_model.py`
- `src/models/model_selection.py`
- `models/final_model.pkl`
- `reports/advanced_model_report.md`
- `docs/day5_model_selection_notes.md`
