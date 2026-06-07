# Day 4 — Model Review Notes

## Summary

The baseline modeling pipeline is sound. `data/processed/feature_dataset.csv` contains only approved pre-delivery features plus the target `sla_breached`, and no leakage columns are present in the final dataset.

## Dataset and feature validation

- Final dataset shape: 96,470 rows, 34 columns.
- Model input `X` uses 33 approved features from `docs/feature_list_v1.md`.
- Target column `sla_breached` is excluded from model inputs and only used for `y`.
- Confirmed leakage columns are not present in the dataset header:
  - `order_delivered_customer_date`
  - `actual_delivery_days`
  - `delivery_delay_days`
  - review-related fields
- Confirmed ID columns and post-delivery fields are removed before modeling by feature builder logic.

## Train/test split and pipeline

- The train/test split is created before model training.
- Split configuration:
  - `test_size=0.2`
  - `random_state=42`
  - `stratify=y`
- Train/test breach rates are consistent:
  - Train rate: 8.11%
  - Test rate: 8.11%
- Preprocessing is fully contained in the model pipeline:
  - Numeric features: median imputation + standard scaling
  - Categorical features: constant imputation with `Unknown` + one-hot encoding with `handle_unknown="ignore"`
  - `purchase_day_of_week` is handled as a categorical feature in the pipeline

## Missing values and encoding

- No missing feature values remain in `X` after dataset creation.
- Feature builder handles missing source values before modeling:
  - location fields are normalized and missing values are filled with explicit categories.
  - numeric product fields are filled with medians.
  - commercial fields are coerced to numeric and missing values are filled.
- Categorical encoding uses one-hot encoding with unknown-category handling, which is appropriate for high-cardinality location and category features.

## Baseline model comparison

The baseline model comparison on the held-out test set is:

- Logistic Regression
  - Recall: 0.6115
  - Precision: 0.1477
  - F1: 0.2379
  - PR-AUC: 0.1825
  - ROC-AUC: 0.7045
- Decision Tree
  - Recall: 0.5738
  - Precision: 0.1297
  - F1: 0.2116
  - PR-AUC: 0.1657
  - ROC-AUC: 0.6690
- Random Forest
  - Recall: 0.6415
  - Precision: 0.1242
  - F1: 0.2081
  - PR-AUC: 0.1630
  - ROC-AUC: 0.6664

### Best baseline model

- Based on the project priority ordering (recall, then precision, then F1, then PR-AUC): `Random Forest` is the best baseline.
- However, Random Forest has the lowest precision and many false positives, so operational usefulness depends on false-alarm tolerance.

## Business interpretation

- Actual SLA breaches caught by the best model: 1,004 true positives.
- Risky orders predicted by the model that were truly breached: 12.4% precision for class 1.
- The model misses too many delayed orders: 561 false negatives, meaning ~35.8% of breaches are still missed.
- The model creates many false alarms: 7,081 false positives for Random Forest.
- Most useful baseline for operations depends on the tradeoff:
  - `Random Forest` is best if recall is the top priority.
  - `Logistic Regression` is more balanced and has slightly higher precision, which may be preferable if false positives are costly.

## Overfitting evaluation

Train vs test comparison shows:

- Logistic Regression: train recall 0.7475 vs test recall 0.6115, indicating some overfitting.
- Decision Tree: train recall 0.7007 vs test recall 0.5738, also indicating overfitting.
- Random Forest: train recall 0.6515 vs test recall 0.6415, showing the most stable generalization among the three.

Overall, the baseline models are not extreme overfitters, but there is a train/test gap and the current performance is modest.

## Day 5 optimization focus

Recommended Day 5 priorities:

1. Improve recall and PR-AUC for the SLA breach class.
2. Reduce false negatives while controlling false positives.
3. Add a threshold/tuning study to align model output with operational risk tolerance.
4. Investigate feature engineering for stronger breach signals, especially around delivery estimates, geography, and order intensity.
5. Consider more advanced categorical encoding or embedding approaches for high-cardinality location features.

## Conclusions

The pipeline is correctly implemented and the baseline models are valid. The next step is to improve predictive power for the breach class and tighten the precision/recall tradeoff for operations.
