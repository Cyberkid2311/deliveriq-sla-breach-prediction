# Feature List v1

Final feature dataset: `data/processed/feature_dataset.csv`

Dataset grain: one row per order.

Target column: `sla_breached`

## Approved Model Features

These fields are allowed as model inputs because they are known before actual customer delivery.

### Time-Based Features

- `purchase_day_of_week`
- `purchase_hour`
- `is_weekend_order`
- `estimated_delivery_days`

### Location-Based Features

- `customer_state`
- `customer_city`
- `seller_state`
- `seller_city`
- `seller_customer_same_state`
- `seller_customer_same_city`

### Product-Based Features

- `product_category_name`
- `product_weight_g`
- `product_weight_kg`
- `total_product_weight_g`
- `total_product_weight_kg`
- `product_length_cm`
- `product_height_cm`
- `product_width_cm`
- `product_volume_cm3`
- `total_product_volume_cm3`
- `product_weight_bucket`
- `product_count`
- `seller_count`
- `product_category_count`

### Commercial And Logistics Features

- `freight_value`
- `avg_freight_value`
- `freight_value_bucket`
- `price`
- `avg_price`
- `item_count`
- `price_per_item`
- `freight_per_item`
- `seller_customer_same_zip_prefix`

## Target Column

- `sla_breached`

Keep this column in the dataset as the prediction target. Do not use it as an input feature.

## Removed Before Modeling

These fields are intentionally excluded from `feature_dataset.csv`.

- `order_id`
- `customer_id`
- `customer_unique_id`
- `order_status`
- `order_approved_at`
- `order_delivered_carrier_date`
- `order_delivered_customer_date`
- `actual_delivery_days`
- `delivery_delay_days`
- Review-related columns
- Other post-delivery columns

## EDA-Only Columns

These fields can be used for analysis and target validation, but they should not be included in model input features.

- `order_delivered_customer_date`
- `actual_delivery_days`
- `delivery_delay_days`
- `order_status`
- `order_approved_at`
- `order_delivered_carrier_date`

## Feature Engineering Notes

- `seller_state` and `seller_city` come from the primary seller fields in the order-level dataset.
- `product_category_name` comes from the primary product category.
- Product weight and dimensions use average product attributes at the order level.
- Total product weight and total product volume are retained to represent shipment-level size.
- `price` and `freight_value` use order-level totals.
- Missing product numeric fields are filled with the column median.
- Missing location and category fields are filled as `unknown`.

## Approval

Feature list v1 is approved for the first modeling dataset.
