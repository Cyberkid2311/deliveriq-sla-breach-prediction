# Day 5 - Model Optimization Notes

## Summary

The Day 5 optimization workflow is implemented. It adds model-safe delivery estimate, route, and order intensity features, trains sklearn-only optimized candidates, and evaluates operating thresholds from 0.05 to 0.95.

The strongest recall-first operational candidate is `Optimized Logistic Regression` at threshold `0.20`.

## Dataset and feature updates

- Final dataset shape after Day 5 feature generation: 96,470 rows, 42 columns.
- New model-safe feature groups:
  - delivery estimate bucket: `estimated_delivery_days_bucket`
  - route pair features: `seller_customer_state_pair`, `seller_customer_city_pair`
  - order intensity buckets: `item_count_bucket`, `product_count_bucket`, `seller_count_bucket`, `price_bucket`, `freight_per_item_bucket`
- The new features are created before delivery and do not use actual delivery dates, delay fields, order status after fulfillment, reviews, or IDs.
- The approved feature list is updated in `docs/feature_list_v1.md`.

## Optimized model candidates

The Day 5 sklearn-only candidates are:

- `Optimized Logistic Regression`
- `Optimized Random Forest`
- `HistGradientBoosting`

Artifacts saved:

- `models/day5_optimized_logistic_regression.pkl`
- `models/day5_optimized_random_forest.pkl`
- `models/day5_hist_gradient_boosting.pkl`
- `models/day5_optimized_best_model.pkl`

Reports saved:

- `reports/day5_model_optimization_report.md`
- `reports/day5_threshold_tuning_report.md`

## Default threshold comparison

At the default threshold, `HistGradientBoosting` has the best PR-AUC but almost no class-1 recall:

| Model | Recall | Precision | F1 | PR-AUC | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| Optimized Logistic Regression | 0.5457 | 0.1676 | 0.2564 | 0.1899 | 0.7084 |
| Optimized Random Forest | 0.6460 | 0.1339 | 0.2219 | 0.1640 | 0.6786 |
| HistGradientBoosting | 0.0019 | 0.6000 | 0.0038 | 0.2078 | 0.7200 |

## Selected recall-first thresholds

The threshold selector uses recall first after basic precision and false-positive guardrails.

| Model | Threshold | Recall | Precision | F1 | PR-AUC | False Positives | False Negatives | True Positives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Optimized Logistic Regression | 0.20 | 0.8843 | 0.1020 | 0.1829 | 0.1899 | 12,188 | 181 | 1,384 |
| Optimized Random Forest | 0.50 | 0.6460 | 0.1339 | 0.2219 | 0.1640 | 6,537 | 554 | 1,011 |
| HistGradientBoosting | 0.05 | 0.8754 | 0.1088 | 0.1935 | 0.2078 | 11,224 | 195 | 1,370 |

## Business interpretation

- Day 4 best baseline Random Forest caught 1,004 breaches and missed 561.
- Day 5 `Optimized Logistic Regression` at threshold `0.20` catches 1,384 breaches and misses 181.
- This reduces false negatives by 380 compared with the Day 4 best baseline.
- The tradeoff is a high false-positive count: 12,188 orders are flagged but are not actual breaches.
- `HistGradientBoosting` is worth keeping as a candidate because it has the strongest PR-AUC, but its default threshold is not operationally useful for recall.

## Recommendation

Use `Optimized Logistic Regression` at threshold `0.20` as the Day 5 recall-first recommendation if operations can tolerate a high alert volume.

If false positives are too costly, use the threshold tuning report to pick a higher threshold or run a Day 6 precision-floor tuning pass.

## Remaining work for Day 6

1. Choose an operational false-positive tolerance with the business team.
2. Add precision-floor threshold tuning, for example maximize recall subject to precision >= 0.12 or 0.15.
3. Add probability calibration so threshold values are easier to interpret.
4. Compare recall-first, F1-first, and precision-floor operating policies side by side.
5. Consider external model/encoding experiments only if dependency changes are allowed.
