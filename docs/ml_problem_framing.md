# ML Problem Framing: SLA Breach Prediction

## 1. Objective

The objective of this project is to predict whether an order is likely to breach its delivery SLA.

An SLA breach means the order was delivered later than the estimated delivery date promised to the customer.

This is a binary classification problem.

The model should predict delay risk early so that business or operations teams can identify risky orders before the delay actually happens.

---

## 2. Target Variable

### Target Column

```python
sla_breached
```

### Target Definition

```text
sla_breached = 1 if order_delivered_customer_date > order_estimated_delivery_date
sla_breached = 0 otherwise
```

### Source Columns

| Column | Meaning |
| --- | --- |
| `order_estimated_delivery_date` | Promised delivery date |
| `order_delivered_customer_date` | Actual customer delivery date |

### Target Interpretation

| sla_breached | Meaning |
| --- | --- |
| 1 | Order breached SLA / delivered late |
| 0 | Order delivered on time or before promised date |

### Notes

For the MVP, only orders with both `order_estimated_delivery_date` and `order_delivered_customer_date` available will be used for model training.

Cancelled, unavailable, or undelivered orders should be handled separately during data cleaning and should not be mixed into the training target without clear logic.

## 3. Prediction Point

The prediction will be made after the order is purchased and before the order is delivered.

For the MVP, the model will use information available at order creation or early shipment stage.

### Prediction Timing

The model should predict SLA breach risk using information available around:

- Order purchase time
- Customer details
- Seller details
- Product details
- Freight/order item details
- Estimated delivery promise

The model should not use any information that is only available after delivery completion.

## 4. Leakage Rules

Data leakage happens when the model uses information that would not be available at the time of prediction.

The following columns must not be used as model input.

| Column | Why Not Use |
| --- | --- |
| `order_delivered_customer_date` | Actual delivery outcome |
| `actual_delivery_time` | Derived from future delivery information |
| `review_score` | Usually created after delivery |
| `delay_reason` | Post-event information |
| `sla_breached` | Target column itself |

### Allowed Feature Examples

The following features can be used because they are available before delivery completion.

| Feature / Column | Why It Is Allowed |
| --- | --- |
| Customer location | Known early |
| Seller location | Known early |
| Product weight | Known early |
| Product dimensions | Known early |
| Freight value | Known early |
| Purchase day/hour | Known early |
| Estimated delivery duration | Known early |

### Columns to Use Carefully

| Column | Caution |
| --- | --- |
| `order_status` | May contain outcome information depending on value |
| `order_delivered_carrier_date` | Only use if prediction point is after carrier handoff |
| `order_approved_at` | Can be used if available before shipment |
| `shipping_limit_date` | Can be used if available early and not derived from final delivery outcome |

## 5. Evaluation Metrics

Accuracy alone is not enough because delayed orders may be fewer than on-time orders.

The main business question is:

> Out of all orders that actually got delayed, how many did our model catch early?

Because of this, recall is very important.

### Metrics to Track

| Metric | Why It Matters |
| --- | --- |
| Recall | Measures how many actual delayed orders the model catches |
| Precision | Measures how many predicted delayed orders were actually delayed |
| F1-score | Balances precision and recall |
| PR-AUC | Useful for imbalanced classification problems |
| Confusion matrix | Easy to explain to business stakeholders |

### Primary Metric

The primary metric for this project is:

```text
Recall
```

Reason:

The business wants to catch as many delayed orders as possible before they breach SLA.

### Secondary Metrics

The secondary metrics are:

- Precision
- F1-score
- PR-AUC
- Confusion matrix

Precision is also important because too many false alerts can reduce trust in the model.

## 6. Final Prediction Output

The final model output should be at order level.

Each order should receive a delay probability and a risk bucket.

### Example Output

| order_id | delay_probability | risk_bucket |
| --- | ---: | --- |
| `abc123` | 0.82 | Critical |
| `def456` | 0.61 | High |
| `ghi789` | 0.33 | Medium |
| `xyz111` | 0.12 | Low |

### Risk Bucket Logic

| Delay Probability | Risk Bucket |
| --- | --- |
| 0.00 - 0.30 | Low |
| 0.31 - 0.60 | Medium |
| 0.61 - 0.80 | High |
| 0.81 - 1.00 | Critical |

### Final Output Columns

| Column | Meaning |
| --- | --- |
| `order_id` | Unique order ID |
| `delay_probability` | Predicted probability of SLA breach |
| `risk_bucket` | Business-friendly risk category |

## 7. Initial Feature Scope for MVP

For the first version, the project should use simple and explainable features.

### Recommended Feature Groups

| Feature Group | Example Features |
| --- | --- |
| Customer location | `customer_city`, `customer_state`, `customer_zip_code_prefix` |
| Seller location | `seller_city`, `seller_state`, `seller_zip_code_prefix` |
| Product details | `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm` |
| Order item details | `price`, `freight_value` |
| Time features | `purchase_day_of_week`, `purchase_hour`, `purchase_month` |
| Promise features | `estimated_delivery_duration_days` |

### Estimated Delivery Duration

This feature can be calculated as:

```text
estimated_delivery_duration_days = order_estimated_delivery_date - order_purchase_timestamp
```

This is allowed because `order_estimated_delivery_date` is known before actual delivery happens.

## 8. Dataset Rules

### Training Data

For MVP training, use delivered orders where these columns are available:

- `order_estimated_delivery_date`
- `order_delivered_customer_date`

### Exclusions for MVP

The following should be excluded or analyzed separately:

- Cancelled orders
- Unavailable orders
- Orders missing actual delivery date
- Orders missing estimated delivery date

These records should not be silently dropped. The count of excluded records should be reported in the data quality report.

