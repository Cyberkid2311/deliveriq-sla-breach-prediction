# Day 4 — Baseline Modeling Preparation and Evaluation Framework

## Objective

The objective of Day 4 is to prepare for baseline machine learning modeling and establish a framework for evaluating model performance in predicting SLA breaches.

The final goal of the modeling phase is to identify orders that are likely to miss their estimated delivery deadlines before the actual delivery occurs.

Target Variable:

```text
sla_breached

0 = SLA Met
1 = SLA Breached
```

Because the target contains two possible classes, this is a binary classification problem.

---

# Dataset Overview

Dataset:

```text
data/processed/feature_dataset.csv
```

Dataset Grain:

```text
One row per order
```

Dataset Size:

```text
Rows: 96,470
```

Target Distribution:

| Class | Meaning      | Count  | Percentage |
| ----- | ------------ | ------ | ---------- |
| 0     | SLA Met      | 88,644 | 91.89%     |
| 1     | SLA Breached | 7,826  | 8.11%      |

---

# Class Imbalance

The dataset is heavily imbalanced because most orders are delivered on time.

```text
91.89% On Time
8.11% Breached
```

This imbalance has important implications for model evaluation.

For example:

```text
If a model predicts every order as "On Time"

Accuracy = 91.89%
```

Despite the high accuracy, the model would fail to identify any delayed deliveries.

Therefore, accuracy alone is not sufficient for evaluating model quality.

For this project, Recall and F1 Score are expected to be more meaningful metrics.

---

# Approved Modeling Features

The final feature set contains only information available before customer delivery.

## Time-Based Features

* purchase_day_of_week
* purchase_hour
* is_weekend_order
* estimated_delivery_days

## Location-Based Features

* customer_state
* customer_city
* seller_state
* seller_city
* seller_customer_same_state
* seller_customer_same_city

## Product-Based Features

* product_category_name
* product_weight_g
* product_weight_kg
* total_product_weight_g
* total_product_weight_kg
* product_length_cm
* product_height_cm
* product_width_cm
* product_volume_cm3
* total_product_volume_cm3
* product_weight_bucket
* product_count
* seller_count
* product_category_count

## Commercial and Logistics Features

* freight_value
* avg_freight_value
* freight_value_bucket
* price
* avg_price
* item_count
* price_per_item
* freight_per_item
* seller_customer_same_zip_prefix

---

# Numerical vs Categorical Features

Machine learning features generally fall into two categories.

## Numerical Features

Numerical features contain measurable values.

Examples:

* freight_value
* avg_freight_value
* price
* avg_price
* estimated_delivery_days
* product_weight_g
* product_volume_cm3
* item_count

Example:

```text
freight_value = 24.50
product_weight_g = 1200
```

These values can be directly used in mathematical calculations.

## Categorical Features

Categorical features represent labels or categories.

Examples:

* customer_state
* customer_city
* seller_state
* seller_city
* product_category_name
* product_weight_bucket
* freight_value_bucket

Example:

```text
customer_state = SP
product_category_name = electronics
```

Categorical variables typically require encoding before being used by machine learning models.

---

# Feature Validation and Leakage Prevention

One of the most important steps before model training is preventing data leakage.

Data leakage occurs when the model receives information that would not be available at prediction time.

The following columns were intentionally removed:

* order_id
* customer_id
* customer_unique_id
* order_status
* order_delivered_customer_date
* actual_delivery_days
* delivery_delay_days
* order_delivered_carrier_date

These fields contain post-delivery information and could allow the model to indirectly learn the target.

The approved feature pipeline ensures only pre-delivery information is used.

---

# Supervised vs Unsupervised Learning

Machine learning algorithms are commonly categorized as supervised or unsupervised learning.

## Supervised Learning

Supervised learning uses historical data where the correct answer is already known.

Example:

```text
Order Features → SLA Breached?
```

The model learns patterns from past observations and applies them to future orders.

This project is a supervised learning problem because every training example contains a known target value:

```text
sla_breached
```

## Unsupervised Learning

Unsupervised learning operates without a target variable.

The objective is to discover hidden patterns within the data.

Common examples:

* Customer Segmentation
* Product Clustering
* Anomaly Detection

Unsupervised learning is not used in the baseline modeling phase of this project.

---

# Correlation vs Causation

Feature analysis performed during Day 3 revealed several relationships with SLA breaches.

Examples:

* Freight Value
* Product Weight
* Customer State
* Seller State

These findings represent correlations.

A correlation indicates that two variables move together.

However:

```text
Correlation ≠ Causation
```

For example:

```text
Higher Freight Value
↓
Higher Breach Rate
```

does not necessarily mean freight cost directly causes delays.

The relationship may instead be driven by:

* Longer delivery distances
* Larger shipments
* Complex logistics routes

Therefore, feature relationships should be interpreted carefully.

---

# Evaluation Metrics

Because the dataset is imbalanced, multiple evaluation metrics will be used.

## Accuracy

Accuracy measures the percentage of total predictions that are correct.

Formula:

```text
(TP + TN) / Total Predictions
```

Accuracy provides a broad overview but may be misleading for imbalanced datasets.

---

## Precision

Precision answers:

```text
When the model predicts an SLA breach,
how often is it correct?
```

Formula:

```text
TP / (TP + FP)
```

Higher precision means fewer false alarms.

---

## Recall

Recall answers:

```text
Out of all actual SLA breaches,
how many did the model successfully identify?
```

Formula:

```text
TP / (TP + FN)
```

Recall is considered one of the most important metrics for this project because missed delays can prevent proactive intervention.

---

## F1 Score

F1 Score balances Precision and Recall.

Formula:

```text
2 × (Precision × Recall) / (Precision + Recall)
```

A high F1 Score indicates strong overall classification performance.

---

# Confusion Matrix

The confusion matrix summarizes prediction outcomes.

| Actual / Predicted | No Breach           | Breach              |
| ------------------ | ------------------- | ------------------- |
| No Breach          | True Negative (TN)  | False Positive (FP) |
| Breach             | False Negative (FN) | True Positive (TP)  |

## Interpretation

### True Negative (TN)

The model correctly predicts an on-time delivery.

### False Positive (FP)

The model predicts a delay that does not occur.

This creates a false alert.

### False Negative (FN)

The model predicts on-time delivery but the order is actually delayed.

This is the most costly prediction error for the business.

### True Positive (TP)

The model correctly predicts a delayed delivery.

---

# Baseline Models

Three baseline classification models will be evaluated.

## Logistic Regression

Logistic Regression is a widely used baseline classification algorithm.

It predicts the probability that an order belongs to a particular class.

Advantages:

* Fast training
* Easy interpretation
* Strong baseline performance
* Efficient on tabular business data

Limitations:

* Assumes mostly linear relationships
* May struggle with complex interactions

---

## Decision Tree

Decision Trees split data into smaller groups using decision rules.

Example:

```text
Freight Value > 50?
        |
      Yes
        |
Product Weight > 5000g?
        |
      Yes
        |
High SLA Breach Risk
```

Advantages:

* Easy to explain
* Handles nonlinear relationships
* Supports both numerical and categorical data

Limitations:

* Can overfit training data
* Sensitive to small data changes

---

## Random Forest

Random Forest combines many Decision Trees into a single ensemble model.

Each tree makes an independent prediction and the final prediction is determined by majority vote.

Advantages:

* Reduced overfitting
* Strong predictive performance
* Handles complex feature interactions
* Often performs well on structured business datasets

Limitations:

* Less interpretable
* Higher computational cost

---

# Expected Evaluation Focus

Model comparison will primarily focus on:

1. Recall for SLA Breach Class (`sla_breached = 1`)
2. Precision for SLA Breach Class
3. F1 Score
4. Business usefulness

Accuracy will be considered but will not be the primary decision criterion.

---

# Model Results

## Logistic Regression

*To be completed after model training.*

## Decision Tree

*To be completed after model training.*

## Random Forest

*To be completed after model training.*

---

# Model Comparison

*To be completed after model training.*

---

# Final Recommendation

*To be completed after model training and evaluation.*
