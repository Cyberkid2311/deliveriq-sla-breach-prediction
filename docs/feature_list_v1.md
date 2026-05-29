# Feature List v1

Source dataset: `data/processed/modeling_dataset_v1.csv`

Dataset grain: one row per order.

Target column: `sla_breached`

## Approved Model Features

These fields are allowed as model inputs because they are known before actual customer delivery.

### Order Timing Features

- `order_purchase_timestamp`
- `order_estimated_delivery_date`
- `estimated_delivery_days`
- `purchase_day_of_week`
- `purchase_hour`
- `is_weekend_order`

### Customer Location Features

- `customer_zip_code_prefix`
- `customer_city`
- `customer_state`

### Seller Location Features

- `seller_count`
- `primary_seller_zip_code_prefix`
- `primary_seller_city`
- `primary_seller_state`

### Product And Item Features

- `item_count`
- `product_count`
- `product_category_count`
- `primary_product_category_name`
- `avg_product_weight_g`
- `avg_product_length_cm`
- `avg_product_height_cm`
- `avg_product_width_cm`
- `avg_product_volume_cm3`

### Price And Freight Features

- `total_price`
- `avg_price`
- `total_freight_value`
- `avg_freight_value`

## Identifier Columns

These columns are useful for tracing records, joins, and debugging. Do not use them as model features.

- `order_id`
- `customer_id`
- `customer_unique_id`
- `primary_product_id`
- `primary_seller_id`

## EDA-Only Columns

These fields can be used for analysis, validation, and reporting, but should not be used as model inputs for the first MVP model.

- `order_status`
- `order_approved_at`
- `order_delivered_carrier_date`
- `order_delivered_customer_date`
- `actual_delivery_days`
- `delivery_delay_days`

## Excluded Leakage Columns

These fields either contain the answer directly or depend on actual post-purchase delivery outcomes.

- `sla_breached`
- `order_delivered_customer_date`
- `actual_delivery_days`
- `delivery_delay_days`

## Day 2 Decision

Feature list v1 is approved for Day 3 feature engineering, with the rule that leakage columns stay out of model input features.
