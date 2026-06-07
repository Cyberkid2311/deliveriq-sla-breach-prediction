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
- `estimated_delivery_days_bucket`

### Location-Based Features

- `customer_state`
- `customer_city`
- `seller_state`
- `seller_city`
- `seller_customer_same_state`
- `seller_customer_same_city`
- `seller_customer_state_pair`
- `seller_customer_city_pair`

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
- `product_count_bucket`
- `seller_count`
- `seller_count_bucket`
- `product_category_count`

### Commercial And Logistics Features

- `freight_value`
- `avg_freight_value`
- `freight_value_bucket`
- `price`
- `avg_price`
- `item_count`
- `item_count_bucket`
- `price_per_item`
- `freight_per_item`
- `price_bucket`
- `freight_per_item_bucket`
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
- Day 5 route features combine seller and customer locations into pre-delivery state/city pair signals.
- Day 5 bucket features discretize estimated delivery days, order counts, price, and per-item freight to capture nonlinear risk patterns.
- `product_category_name` comes from the primary product category.
- Product weight and dimensions use average product attributes at the order level.
- Total product weight and total product volume are retained to represent shipment-level size.
- `price` and `freight_value` use order-level totals.
- Missing product numeric fields are filled with the column median.
- Missing location and category fields are filled as `unknown`.

**Day 3: Feature validation summary**

- **Modeling dataset checked:** `data/processed/modeling_dataset_v1.csv` (96470 rows, 40 columns).
- **Dataset grain:** one row per order — `order_id` is unique (0 duplicates).
- **Target (`sla_breached`) distribution:** 0 = 88644 (91.89%), 1 = 7826 (8.11%).
- **Newly available order-level fields (present in modeling dataset):** `product_count`, `seller_count`, `product_category_count`, `avg_price`, `avg_freight_value`.
- **Derived fields created at feature-build time:** `price_per_item`, `freight_per_item`, `seller_customer_same_zip_prefix` (computed during `src/features/build_features.py`).
- **Columns with missing values (>0):** `order_approved_at` (0.0145%), `order_delivered_carrier_date` (0.0010%), `avg_product_weight_g` / `avg_product_length_cm` / `avg_product_height_cm` / `avg_product_width_cm` / `avg_product_volume_cm3` (~0.0166% each).
- **Categorical cardinalities:** `customer_state` = 27, `customer_city` = 4085 (top cities: Sao Paulo, Rio de Janeiro, Belo Horizonte).
- **Leakage columns present in the modeling dataset:** many of the raw identifiers and post-delivery fields (these are removed before creating the final `feature_dataset.csv`).

See `docs/day3_feature_validation_notes.md` for detailed counts, missing-value percentages, and top categorical values.

## Approval

Feature list v1 is approved for the first modeling dataset.
