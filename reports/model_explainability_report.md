# Model Explainability Report

## Summary

The final model is explained using model-native feature importance. SHAP analysis is attempted when the optional `shap` package is available.

## Top 10 Model Drivers

| Rank | Feature | Importance | Business Explanation |
| ---: | --- | ---: | --- |
| 1 | `numeric__estimated_delivery_days` | 1099.000000 | Long promised delivery window |
| 2 | `categorical__customer_city` | 651.000000 | Historical pattern learned from approved pre-delivery features |
| 3 | `categorical__customer_state` | 606.000000 | Destination region pattern |
| 4 | `numeric__avg_freight_value` | 531.000000 | Costlier or more complex shipment |
| 5 | `numeric__product_length_cm` | 433.000000 | Historical pattern learned from approved pre-delivery features |
| 6 | `categorical__seller_city` | 417.000000 | Historical pattern learned from approved pre-delivery features |
| 7 | `categorical__seller_customer_city_pair` | 402.000000 | Historical pattern learned from approved pre-delivery features |
| 8 | `numeric__avg_price` | 397.000000 | Historical pattern learned from approved pre-delivery features |
| 9 | `categorical__product_category_name` | 377.000000 | Product category delay pattern |
| 10 | `numeric__price` | 374.000000 | Historical pattern learned from approved pre-delivery features |

## SHAP Status

SHAP was not run because the optional `shap` package is not installed.

## Example High-Risk Explanation

A high-risk order may be flagged because it combines signals such as a cross-state route, high freight value, long estimated delivery window, heavier shipment, or a historically riskier destination/product pattern.
