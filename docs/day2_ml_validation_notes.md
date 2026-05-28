# Day 2 ML Validation Notes

## Task 1 - SLA Target Validation

The current `sla_breached` target is created in `src/data/process_data.py` using a full timestamp comparison:

```py
orders["sla_breached"] = np.where(
    (
        orders["order_delivered_customer_date"].notna()
        & orders["order_estimated_delivery_date"].notna()
        & (
            orders["order_delivered_customer_date"]
            > orders["order_estimated_delivery_date"]
        )
    ),
    1,
    0,
)
```

### Target Distribution

Source: `data/gold/olist_final_consumption_dataset.csv`

| SLA Breached | Count | Percentage |
| --- | ---: | ---: |
| 0 | 103,935 | 92.26% |
| 1 | 8,715 | 7.74% |

Current breach rate:

```text
8,715 / 112,650 = 7.74%
```

### Timestamp vs Date-Only Check

| Target logic | Breached rows | Breach rate |
| --- | ---: | ---: |
| Full timestamp comparison | 8,715 | 7.74% of all rows |
| Calendar date-only comparison | 7,265 | 6.45% of all rows |

Difference:

```text
1,450 rows
```

These 1,450 rows were delivered on the same calendar day as the estimated delivery date, but after midnight. Because `order_estimated_delivery_date` is stored as a date at `00:00:00`, the full timestamp comparison marks them as late.

### Validation Answers

| Question | Answer |
| --- | --- |
| What percentage of orders are breached? | Current logic: 7.74%. Date-only logic: 6.45%. |
| Are there too many late orders? | No. The breach rate is below 10%, but the current timestamp logic inflates the target by 1,450 rows. |
| Are there too few late orders? | The positive class is small enough to require imbalance-aware evaluation, but not so small that modeling is blocked. |
| Are same-day dates handled correctly? | No. Same-calendar-day deliveries after midnight are currently marked as breaches. |
| Are timestamps or only dates being compared? | Timestamps are currently compared. SLA logic should use calendar dates or treat the estimate as end-of-day. |

### Recommended Target Rule

Use calendar-day SLA semantics: an order is breached only when the delivered date is after the estimated delivery date.

```py
orders["sla_breached"] = np.where(
    (
        orders["order_delivered_customer_date"].notna()
        & orders["order_estimated_delivery_date"].notna()
        & (
            orders["order_delivered_customer_date"].dt.date
            > orders["order_estimated_delivery_date"].dt.date
        )
    ),
    1,
    0,
)
```

Alternative: normalize `order_estimated_delivery_date` to end-of-day before comparing timestamps.

## Task 2 - Day 2 Leakage Rules

### Allowed for Modeling

These columns are safe because they are known before delivery:

- `order_purchase_timestamp`
- `order_estimated_delivery_date`
- `customer_state`
- `customer_city`
- `customer_zip_code_prefix`
- `seller_state`
- `seller_city`
- `seller_zip_code_prefix`
- `product_category_name`
- `product_weight_g`
- `product_length_cm`
- `product_height_cm`
- `product_width_cm`
- `freight_value`
- `price`
- `estimated_delivery_days`
- `purchase_day_of_week`
- `purchase_hour`
- `is_weekend_order`

Notes:

- The current gold dataset uses `purchase_dayofweek`; the modeling dataset should rename it to `purchase_day_of_week` or document the mapping.
- `freight_value` and `price` are approved model features because they are known before delivery, but they are not present in the current gold consumption dataset reviewed in `reports/eda_summary.md`.

### EDA-Only Columns

These columns may be used for analysis and validation, but not as model inputs:

- `order_delivered_customer_date`
- `order_approved_at`
- `order_delivered_carrier_date`
- `carrier_handover_days`
- `actual_delivery_days`
- `delivery_delay_days`
- `review_score`
- `customer_review_comment`
- `order_status`

### Excluded Leakage Columns

These columns either contain the answer directly or are only known after delivery:

- `order_delivered_customer_date`
- `actual_delivery_days`
- `delivery_delay_days`
- `review_score`
- `customer_review_comment`
- `sla_breached`

## Task 3 - Class Imbalance Review

Using the current gold target:

| SLA Breached | Count | Percentage |
| --- | ---: | ---: |
| 0 | 103,935 | 92.26% |
| 1 | 8,715 | 7.74% |

Using the recommended date-only target:

| SLA Breached | Count | Percentage |
| --- | ---: | ---: |
| 0 | 105,385 | 93.55% |
| 1 | 7,265 | 6.45% |

Decision:

| Situation | Applies? | Action |
| --- | --- | --- |
| Breach rate is less than 10% | Yes | Use recall, PR-AUC, class weights, stratified splits, and threshold tuning. |
| Breach rate is 10-30% | No | Not the current situation. |
| Breach rate is above 40% | No | No evidence of severe target logic failure from the overall rate. |

The target is imbalanced. The first model should prioritize breached-order recall and PR-AUC rather than accuracy alone.

## Task 4 - First Model Input List

The companion deliverable is `docs/feature_list_v1.md`. It should remain the approved source for:

1. Approved model features
2. EDA-only columns
3. Excluded leakage columns

## Task 5 - Day 2 Output Review

### `reports/eda_summary.md`

Feedback:

- Target column: The report correctly shows the current `sla_breached` distribution as 8,715 breached rows and a 7.74% breach rate, but it should mention that this is based on timestamp comparison and may overstate same-day breaches.
- Dataset grain: The report uses `data/gold/olist_final_consumption_dataset.csv`, which has 112,650 rows and 98,666 unique orders. This is not one row per order.
- Missing values: Critical target date fields are mostly clean: `order_purchase_timestamp` has 0 missing values, `order_estimated_delivery_date` has 0, and `order_delivered_customer_date` has 2,454 missing values.
- Leakage: Delivery outcome and review columns should stay out of model features.
- EDA findings: Regional, purchase-day, category, and distance-delay patterns are meaningful, but seller-state and category findings should be interpreted with sample-size caution.

### `data/processed/modeling_dataset_v1.csv`

Feedback:

- This file is currently missing from the repo and could not be reviewed directly.
- Until it exists, use `data/gold/base_order_dataset.csv` as the one-row-per-order reference. It has 98,666 rows and 98,666 unique orders.
- The future modeling dataset should exclude leakage columns from features while retaining `sla_breached` only as the target.
- The modeling dataset should apply or document the date-only SLA target correction before training.

## Final Day 2 Decisions

- Current `sla_breached` logic is not fully correct for calendar-day SLA semantics because it compares timestamps.
- The recommended target is date-only delivery date greater than date-only estimated delivery date.
- The breach rate is below 10%, so the model should use recall, PR-AUC, class weights, stratified splitting, and threshold tuning.
- Approved model features are limited to fields known before delivery.
- Delivery outcomes, review information, and the target itself must not be used as model input features.
