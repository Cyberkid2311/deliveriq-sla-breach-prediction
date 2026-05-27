# Data Quality Report

## Objective

Evaluate the quality and usability of the raw Olist datasets before any exploratory analysis or machine learning work.

The following checks were performed:

- Missing values
- Duplicate rows
- Date-related fields
- Date format consistency

---

# 1. olist_customers_dataset.csv

## Missing Values

No missing values detected.

## Duplicate Rows

Duplicate rows: **0**

## Date Columns

No date-related columns detected.

## Observations

- Dataset appears complete.
- Customer location fields are fully populated.
- No immediate data quality concerns identified.


---

# 2. olist_geolocation_dataset.csv

## Missing Values

No missing values detected.

## Duplicate Rows

Duplicate rows: **261,831**

## Date Columns

No date-related columns detected.

## Observations

- Dataset contains a large number of duplicate records.
- Duplicates are not immediately considered data errors.
- Since geolocation information is region-based, repeated ZIP code and coordinate combinations may naturally occur.
- Requires validation before deciding whether duplicates should be removed.


---

# 3. olist_order_items_dataset.csv

## Missing Values

No missing values detected.

## Duplicate Rows

Duplicate rows: **0**

## Date Columns

Detected:

- shipping_limit_date

## Date Validation

Result:

- No invalid date formats detected.

Observed format:

```text
YYYY-MM-DD HH:MM:SS
```

Example:

```text
2017-09-19 09:45:35
```

## Observations

- Shipping timestamps appear consistently formatted.
- Dataset appears clean and ready for downstream analysis.


---

# 4. olist_orders_dataset.csv

## Missing Values

Detected:

| Column | Missing |
|--------|--------|
| order_approved_at | 160 |
| order_delivered_carrier_date | 1783 |
| order_delivered_customer_date | 2965 |

## Duplicate Rows

Duplicate rows: **0**

## Date Columns

Detected:

- order_purchase_timestamp
- order_approved_at
- order_delivered_carrier_date
- order_delivered_customer_date
- order_estimated_delivery_date

## Date Validation

Validation performed after excluding missing values.

Result:

- No invalid date formats detected.

Observed format:

```text
YYYY-MM-DD HH:MM:SS
```

Example:

```text
2017-10-02 10:56:33
```

## Additional Findings

Observed that:

```text
order_estimated_delivery_date
```

contains values similar to:

```text
2017-10-18 00:00:00
```

Observation:

- Estimated delivery values consistently use midnight timestamps (`00:00:00`).
- This suggests the field likely stores delivery dates rather than meaningful delivery times.

## Interpretation of Missing Dates

Missing values in delivery-related columns are not automatically considered data errors.

Possible reasons include:

- Cancelled orders
- Orders not yet delivered
- Incomplete order lifecycle records

Further validation may be performed during later project stages.

## Observations

- This dataset contains the most time-sensitive information.
- Delivery timeline information appears internally consistent.
- Suitable candidate for SLA-related analysis.


---

# 5. olist_products_dataset.csv

## Missing Values

Detected:

| Column | Missing |
|--------|--------|
| product_category_name | 610 |
| product_name_lenght | 610 |
| product_description_lenght | 610 |
| product_photos_qty | 610 |
| product_weight_g | 2 |
| product_length_cm | 2 |
| product_height_cm | 2 |
| product_width_cm | 2 |

## Duplicate Rows

Duplicate rows: **0**

## Date Columns

No date-related columns detected.

## Observations

- Missing values appear concentrated across related product metadata columns.
- Product dimensions are nearly complete.
- Missing product descriptions and categories may require handling later.


---

# 6. olist_sellers_dataset.csv

## Missing Values

No missing values detected.

## Duplicate Rows

Duplicate rows: **0**

## Date Columns

No date-related columns detected.

## Observations

- Dataset appears complete.
- Seller location information is fully available.
- No immediate data quality concerns identified.


---

# Overall Findings

## Missing Values

Missing values exist primarily in:

- Delivery timeline fields
- Product metadata fields

Most datasets contain no missing data.

## Duplicate Records

Only the geolocation dataset contains substantial duplicates.

## Date Quality

All detected date-related columns:

- Were successfully parsed
- Showed no invalid formats after excluding missing values
- Followed a consistent structure:

```text
YYYY-MM-DD HH:MM:SS
```

## Conclusion

Overall data quality is acceptable for exploratory analysis.

Several fields require contextual interpretation rather than immediate cleaning, particularly:

- delivery timestamps
- geolocation duplicates
- missing product metadata