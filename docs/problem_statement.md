# Problem Statement

## Business Problem

E-commerce customers expect orders to arrive by the promised delivery date. When deliveries miss their SLA, customers may contact support, lose trust in the marketplace, or choose a competitor in the future.

Operations teams need an early warning system that identifies orders likely to breach SLA before the delay happens. This allows teams to monitor, prioritize, or intervene on risky deliveries.

## Project Objective

Build an end-to-end machine learning system that predicts whether an order is likely to breach its promised delivery SLA and converts that prediction into an operational risk score.

## Target User

The primary user is a logistics or operations team member who needs to identify risky orders early and decide which deliveries should be monitored or prioritized.

## ML Objective

This is a binary classification problem:

- `0`: order is expected to meet SLA
- `1`: order is expected to breach SLA

The model predicts `sla_breached` using only information available before customer delivery.

## Success Criteria

The project is successful if it:

- creates a leakage-safe SLA breach target
- trains and compares baseline and advanced models
- prioritizes recall for the SLA breach class
- saves a final model artifact
- generates order-level SLA breach probabilities
- assigns business-friendly risk buckets
- provides explainability and a dashboard for review

## Business Tradeoff

The project intentionally prioritizes recall because missing a risky order can be costly. This creates more false positives, so the final operating threshold should be reviewed against operations capacity before production use.
