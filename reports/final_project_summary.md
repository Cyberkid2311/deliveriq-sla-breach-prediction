# Final Project Summary

## Project Overview

DeliverIQ is an end-to-end machine learning project for predicting e-commerce delivery SLA breaches. It converts historical Olist order, customer, seller, product, freight, and delivery data into risk scores that operations teams can use to identify deliveries that may need early intervention.

## Dataset

The project uses the Olist e-commerce dataset. The raw data includes order lifecycle timestamps, customer and seller locations, product metadata, item-level prices, and freight values.

The final modeling dataset is `data/processed/feature_dataset.csv`.

- Rows: 96,470
- Grain: one row per order
- Target: `sla_breached`
- Target rate: 8.11% breached orders

## SLA Breach Definition

`sla_breached` identifies whether an order missed its promised delivery SLA. Post-delivery fields used to validate or create the target are not used as model input features.

## EDA Insights

The exploratory analysis found that:

- Most orders were delivered successfully.
- SLA breaches are relatively rare, making the problem imbalanced.
- Some customer states have much higher breach rates than the overall average.
- Certain seller states and product categories show elevated delivery risk.
- Longer delivery distances and route complexity are associated with higher breach probability.
- Monday purchases showed slightly higher SLA breach rates than other purchase days.

These findings motivated geography, route, delivery estimate, product, freight, and order intensity features.

## Feature Engineering

The final model uses pre-delivery features only:

- purchase timing
- estimated delivery duration
- customer and seller location
- seller-customer route pairs
- product category, weight, volume, and count
- freight and price features
- bucketed delivery, price, freight, item, product, and seller counts

Leakage columns such as actual delivery date, delay duration, reviews, and IDs are excluded from model inputs.

## Modeling Results

The project trained baseline and advanced sklearn models:

- Logistic Regression
- Decision Tree
- Random Forest
- Optimized Logistic Regression
- Tuned Random Forest
- HistGradientBoosting

The final selected model is Logistic Regression with a tuned threshold of `0.25`.

| Metric | Value |
| --- | ---: |
| Recall class 1 | 0.8914 |
| Precision class 1 | 0.1005 |
| F1 class 1 | 0.1806 |
| PR-AUC | 0.1825 |
| False negatives | 170 |
| False positives | 12,488 |

The final model favors catching likely SLA breaches, which fits the logistics goal of early risk detection.

## Risk Scoring Output

The final prediction workflow creates `data/predictions/delivery_risk_scores.csv` with:

- `order_id`
- `sla_breach_probability`
- `risk_bucket`
- `customer_state`
- `seller_state`
- `product_category_name`
- `estimated_delivery_days`
- `top_risk_reason`

Risk bucket distribution:

| Risk Bucket | Orders |
| --- | ---: |
| Low | 34,891 |
| Medium | 41,184 |
| High | 16,412 |
| Critical | 3,983 |

## Dashboard

The dashboard in `dashboard/app.py` helps users review risk scores by bucket, geography, product category, and individual high-risk orders. It includes filters so operations teams can focus on specific states, categories, and risk levels.

## Explainability

The project includes model-native feature importance in `reports/model_feature_importance.csv` and `reports/model_explainability_report.md`. The report translates model signals into business-friendly explanations such as route complexity, high freight value, long promised delivery windows, and destination/product patterns.

## Conclusion

DeliverIQ is ready as a portfolio-ready ML project. It demonstrates data preparation, target validation, feature engineering, model training, model selection, risk scoring, explainability, and dashboard delivery in one reproducible workflow.
