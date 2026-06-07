# Project Learnings

## Technical Learnings

- Target validation matters before modeling. The SLA breach definition depends on delivery and estimated delivery date semantics.
- Leakage prevention is central in delivery prediction. Actual delivery dates, delay duration, order status after fulfillment, reviews, and IDs must not be used as model inputs.
- Imbalanced classification needs different metrics. Accuracy is not enough when only a small percentage of orders breach SLA.
- Threshold tuning can matter as much as model choice. Lower thresholds caught many more risky orders but increased false positives.
- Preprocessing should live inside the model pipeline so training and prediction use the same transformations.

## Business Learnings

- A high-recall model is useful only if operations can handle the alert volume.
- Risk buckets are easier for business users to act on than raw probabilities alone.
- Geography, route complexity, product category, freight value, and delivery promise length are useful ways to explain risk.
- Model output becomes more valuable when paired with dashboard filters and simple explanations.

## Project Execution Learnings

- Building in day-by-day deliverables made the project easier to validate.
- Reports and notes are important for making a portfolio project understandable.
- Reproducible scripts are more reliable than notebook-only workflows.
- A complete ML project should include model training, prediction output, explainability, and a dashboard.

## Main Tradeoff

The final model is recall-focused. It catches most SLA breaches but creates many false positives. This is acceptable for an early warning system only if operations values broad coverage and has enough capacity to review flagged orders.
