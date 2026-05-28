# Feature List v1

## 1. Approved Model Features

These fields are allowed for modeling because they are known before delivery.

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
- `freight_value` and `price` are approved because they are pre-delivery fields, but they are not present in the current gold consumption dataset reviewed on Day 2.

## 2. EDA-Only Columns

These fields can be used for analysis, target validation, and reporting, but must not be included as model input features.

- `order_delivered_customer_date`
- `order_approved_at`
- `order_delivered_carrier_date`
- `carrier_handover_days`
- `actual_delivery_days`
- `delivery_delay_days`
- `review_score`
- `customer_review_comment`
- `order_status`

## 3. Excluded Leakage Columns

These fields must not be used as model input features because they either contain the answer directly or are only known after delivery.

- `order_delivered_customer_date`
- `actual_delivery_days`
- `delivery_delay_days`
- `review_score`
- `customer_review_comment`
- `sla_breached`
