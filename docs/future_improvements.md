# Future Improvements

## Model Improvements

- Add probability calibration so predicted probabilities are easier to interpret.
- Try LightGBM, XGBoost, or CatBoost if additional dependencies are allowed.
- Add target encoding or frequency encoding for high-cardinality city and route features.
- Use cross-validation instead of a single train/test split for more stable model selection.
- Tune thresholds with explicit business constraints such as maximum alerts per day or minimum precision.

## Feature Improvements

- Add richer geography features such as distance, region groupings, and route-level historical delay rates.
- Add seller reliability history using only information available before each order.
- Add product category historical delay features with leakage-safe time windows.
- Add calendar and seasonality features such as holidays, month, and sales periods.
- Add freight-to-price and weight-to-freight ratios for shipment complexity.

## Evaluation Improvements

- Report calibration curves and lift charts.
- Compare recall-first, F1-first, and precision-floor operating policies.
- Track alert volume by risk bucket.
- Add model stability checks across time periods or geographies.
- Add fairness-style review across customer states to detect uneven performance.

## Dashboard Improvements

- Add downloadable filtered high-risk order lists.
- Add trend views by month or week.
- Add map-based views for risky routes.
- Add drill-down pages for individual order explanations.
- Add user-controlled threshold sliders.

## Engineering Improvements

- Add automated tests for feature schema, leakage checks, model training, and prediction output.
- Add CI checks for formatting and script execution.
- Save model metadata with training date, feature list, metrics, and selected threshold.
- Add a Makefile or task runner for the full pipeline.
- Add Docker support for easier dashboard deployment.

## Business Rollout Improvements

- Validate risk thresholds with operations teams.
- Estimate the cost of false positives versus false negatives.
- Define action playbooks for Medium, High, and Critical risk orders.
- Monitor model performance after deployment.
- Retrain periodically as seller, customer, and logistics patterns change.
