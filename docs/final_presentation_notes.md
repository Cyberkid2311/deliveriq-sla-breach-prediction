# Final Presentation Notes

## One-Minute Project Pitch

DeliverIQ predicts whether an e-commerce order is likely to miss its promised delivery SLA. The project turns historical Olist logistics data into early risk scores and risk buckets so operations teams can prioritize risky deliveries before they become customer problems.

## Problem Story

Late deliveries create avoidable customer dissatisfaction and support workload. The business needs a way to identify risky orders early, not only analyze delays after they happen.

## ML Framing

This is a binary classification problem:

- `0`: order is not expected to breach SLA
- `1`: order is likely to breach SLA

Because breaches are uncommon, the project does not optimize for accuracy. It prioritizes recall for the breach class so the model catches more risky orders.

## End-To-End Workflow

```text
Raw Olist Dataset
        |
Data Cleaning
        |
SLA Breach Target Creation
        |
Feature Engineering
        |
Baseline Modeling
        |
Advanced Modeling
        |
Model Selection
        |
Risk Scoring
        |
Explainability
        |
Dashboard
```

## Key EDA Findings

- SLA breaches are a minority class.
- Geography is important: some customer and seller states show higher breach rates.
- Longer and more complex delivery routes increase risk.
- Product category, freight value, and order intensity can influence delivery risk.

## Feature Engineering Story

The model uses only pre-delivery features:

- estimated delivery duration
- customer and seller location
- route pair signals
- product category and physical characteristics
- freight and price fields
- order count and intensity buckets

No actual delivery date, delay duration, review fields, or IDs are used as inputs.

## Model Results

The final model is LightGBM Classifier with a tuned threshold of `0.25`.

Key results:

- Recall class 1: 0.9137
- Precision class 1: 0.1000
- False negatives: 135
- False positives: 12,865

The model catches most true SLA breaches, but it creates a high number of alerts. This is acceptable only if operations prefers broad early warning over missing risky orders.

## Dashboard Story

The dashboard converts model output into business-facing risk buckets:

- Low: no action
- Medium: monitor
- High: prioritize
- Critical: immediate intervention

Users can filter by customer state, seller state, product category, and risk bucket.

## Interview Explanation

I built this project as a complete ML workflow, not just a model. I validated the target, removed leakage, engineered pre-delivery features, compared baseline and advanced models, tuned decision thresholds for the business objective, generated order-level risk scores, added explainability, and built a Streamlit dashboard. The most important tradeoff was recall versus false positives: the final model catches most SLA breaches, but operations would need to decide whether the alert volume is acceptable.

## Resume-Ready Description

Built an end-to-end logistics SLA breach prediction system using the Olist e-commerce dataset. Engineered pre-delivery order, route, product, freight, and timing features; trained and compared baseline models plus LightGBM and XGBoost; selected a recall-focused final model with threshold tuning; generated order-level risk scores and risk buckets; and delivered explainability reports plus a Streamlit dashboard for operations review.
