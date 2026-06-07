# Day 5 Model Selection Notes

## Validation

- Source dataset: `data\processed\feature_dataset.csv`
- Target: `sla_breached`
- Split: stratified 20% holdout using the same Day 4 logic.
- Preprocessing is contained inside sklearn pipelines.
- Final model inputs use approved pre-delivery features only.

## Final Decision

- Selected model: `Logistic Regression`
- Final artifact: `models/final_model.pkl`
- Selected threshold: 0.25

The final model is selected by the project priority order: recall, precision, F1-score, PR-AUC, ROC-AUC, stability, explainability, and ease of deployment.

## Baseline Versus Final Model

- Best Day 4 baseline by recall: `Random Forest` with recall 0.6415.
- Final model threshold recall: 0.8914.
- Final model threshold precision: 0.1005.
- Final model false negatives: 170.
- Final model false positives: 12488.

## Threshold Strategy

The project uses a tuned probability threshold rather than relying only on 0.50. Lower thresholds catch more risky orders but create more false alerts. The selected threshold is intended for recall-first operations.

## Risk Bucket Logic

| Probability Range | Risk Bucket | Action |
| ---: | --- | --- |
| 0.00-0.30 | Low | No action |
| >0.30-0.60 | Medium | Monitor |
| >0.60-0.80 | High | Prioritize |
| >0.80-1.00 | Critical | Immediate intervention |

## Day 6 Readiness

The model is ready for Day 6 risk scoring, explainability, and dashboard work.
