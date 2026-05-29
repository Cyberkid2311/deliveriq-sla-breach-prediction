# Day 3 — Feature Validation Notes

Checked: `data/processed/modeling_dataset_v1.csv`

Summary
- Rows: 96,470
- Columns: 40
- One row per order: `order_id` is unique (96,470 unique IDs, 0 duplicates).
- Target distribution (`sla_breached`):
  - 0: 88,644 (91.887%)
  - 1: 7,826 (8.113%)

Newly available and derived fields
- Present in modeling dataset (ready for feature-building):
  - `product_count` (int)
  - `seller_count` (int)
  - `product_category_count` (int)
  - `avg_price` (float)
  - `avg_freight_value` (float)

- Created during `src/features/build_features.py` (not present in raw modeling CSV):
  - `price_per_item` = `price` / `item_count`
  - `freight_per_item` = `freight_value` / `item_count`
  - `seller_customer_same_zip_prefix` = compare `primary_seller_zip_code_prefix` and `customer_zip_code_prefix`

Missing value overview (columns with non-zero missing percent)
- `order_approved_at`: 0.0145%
- `order_delivered_carrier_date`: 0.0010%
- `avg_product_weight_g`: 0.0166%
- `avg_product_length_cm`: 0.0166%
- `avg_product_height_cm`: 0.0166%
- `avg_product_width_cm`: 0.0166%
- `avg_product_volume_cm3`: 0.0166%

Categorical cardinality and top values
- `customer_state`: 27 unique values — top 5 states:
  1. SP (40,494)
  2. RJ (12,350)
  3. MG (11,354)
  4. RS (5,344)
  5. PR (4,923)
- `customer_city`: 4,085 unique values — top 5 cities:
  1. sao paulo (15,045)
  2. rio de janeiro (6,601)
  3. belo horizonte (2,697)
  4. brasilia (2,071)
  5. curitiba (1,489)

Leakage check
- The modeling CSV contains several raw identifiers and post-delivery fields used for target creation and EDA (e.g. `order_id`, `customer_id`, `order_approved_at`, `order_delivered_customer_date`, `actual_delivery_days`). These are flagged as leakage for model input — they are removed by the feature builder before saving the final `feature_dataset.csv`.

Approval / Recommendations
- The final feature pipeline in `src/features/build_features.py` produces an approved, model-safe feature set (`docs/feature_list_v1.md`) by mapping source columns and creating derived features.
- Add a quick validation unit test that asserts:
  - `order_id` uniqueness in modeling dataset
  - Required source columns exist
  - No leakage columns in the final `feature_dataset.csv`
- Consider computing `price_per_item` and `freight_per_item` in the modeling dataset if you want to inspect their distributions earlier, otherwise computing them at feature-build time is fine.

Full diagnostics were computed programmatically; if you want the raw diagnostic JSON, I can attach it or commit it here.

-- Automated feature validation (Day 3)
