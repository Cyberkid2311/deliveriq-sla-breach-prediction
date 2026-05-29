# Day 2 ML Validation Notes

## Objective

Day 2 answers this question:

Can we create a clean dataset where each row is one order and each order has a correct SLA breach label?

Answer: yes.

The completed modeling dataset is:

```text
data/processed/modeling_dataset_v1.csv
```

## Deliverables Check

| Deliverable | Status |
| --- | --- |
| `notebooks/02_data_cleaning_and_eda.ipynb` | Complete |
| `notebooks/02_create_target_and_modeling_dataset.ipynb` | Complete |
| `src/features/create_target.py` | Complete |
| `data/processed/modeling_dataset_v1.csv` | Complete |
| `reports/eda_summary.md` | Complete |
| `docs/feature_list_v1.md` | Complete |
| `docs/day2_ml_validation_notes.md` | Complete |

## Modeling Dataset Review

Source: `data/processed/modeling_dataset_v1.csv`

| Check | Result |
| --- | ---: |
| Rows | 96,470 |
| Columns | 38 |
| Duplicate `order_id` rows | 0 |
| Order statuses included | `delivered` only |
| Missing `order_delivered_customer_date` | 0 |
| Missing `order_estimated_delivery_date` | 0 |

The dataset is one row per order and is suitable for the first MVP modeling dataset.

## Target Logic Validation

The Day 2 task defines the target as:

```py
sla_breached = 1 if order_delivered_customer_date > order_estimated_delivery_date
sla_breached = 0 otherwise
```

This target is created in `src/features/create_target.py`.

Validation result:

| Check | Result |
| --- | ---: |
| Target values are binary | Yes |
| Mismatches from requested timestamp rule | 0 |
| Missing target values | 0 |

## Target Distribution

| `sla_breached` | Count | Percentage |
| --- | ---: | ---: |
| 0 | 88,644 | 91.89% |
| 1 | 7,826 | 8.11% |

The positive class is below 10%, so Day 3 modeling should use metrics and methods that handle class imbalance.

Recommended evaluation focus:

- Recall for breached orders
- Precision-recall AUC
- F1 score
- Stratified train/test split
- Class weights or threshold tuning

## Created Time-Based Columns

The following columns were created successfully:

- `sla_breached`
- `estimated_delivery_days`
- `actual_delivery_days`
- `delivery_delay_days`
- `purchase_day_of_week`
- `purchase_hour`
- `is_weekend_order`

Important leakage decision:

- `estimated_delivery_days`, `purchase_day_of_week`, `purchase_hour`, and `is_weekend_order` are model-safe.
- `actual_delivery_days` and `delivery_delay_days` are EDA-only because they depend on the actual delivery date.

## Leakage Review

The following fields must not be used as model inputs:

- `sla_breached`
- `order_delivered_customer_date`
- `actual_delivery_days`
- `delivery_delay_days`

The following fields are also EDA-only for the MVP:

- `order_status`
- `order_approved_at`
- `order_delivered_carrier_date`

Reason:

The MVP predicts delivery SLA risk from information available before final delivery. Any feature that depends on actual delivery timing would leak the answer into the model.

## EDA Review

The existing EDA deliverables are present:

- `notebooks/02_data_cleaning_and_eda.ipynb`
- `reports/eda_summary.md`

Key summarized patterns from the EDA:

- SLA breaches are a minority class.
- Missing actual delivery dates are associated with non-delivered orders.
- Regional delivery patterns differ by customer and seller location.
- Product categories show different delay patterns.
- Longer-distance deliveries tend to have higher SLA breach risk in the existing EDA summary.

## Day 2 Success Criteria

| Success Criteria | Status |
| --- | --- |
| SLA breach target is created | Complete |
| Target logic is validated | Complete |
| Modeling dataset has one row per order | Complete |
| Only delivered orders are used for MVP | Complete |
| Leakage columns are clearly excluded | Complete |
| Basic EDA charts are completed | Complete |
| Delay patterns are summarized | Complete |
| Feature list v1 is approved | Complete |
| Dataset is ready for Day 3 feature engineering | Complete |

## Final Day 2 Decision

Day 2 is complete. The repository now contains a clean one-row-per-order modeling dataset with a validated SLA breach target and documented model-safe features.
