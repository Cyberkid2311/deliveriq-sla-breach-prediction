# Model Explainability Report

## Summary

The final model is explained using model-native feature importance. SHAP analysis is attempted when the optional `shap` package is available.

## Top 10 Model Drivers

| Rank | Feature | Importance | Business Explanation |
| ---: | --- | ---: | --- |
| 1 | `categorical__customer_city_santa cruz de goias` | 3.740506 | Historical pattern learned from approved pre-delivery features |
| 2 | `categorical__customer_city_arace` | 2.962578 | Historical pattern learned from approved pre-delivery features |
| 3 | `categorical__seller_city_terra boa` | 2.789364 | Historical pattern learned from approved pre-delivery features |
| 4 | `categorical__customer_city_capela do alto` | 2.636775 | Historical pattern learned from approved pre-delivery features |
| 5 | `categorical__customer_city_senges` | 2.570985 | Historical pattern learned from approved pre-delivery features |
| 6 | `categorical__customer_city_japi` | 2.567078 | Historical pattern learned from approved pre-delivery features |
| 7 | `categorical__customer_city_sao joao de iracema` | 2.483716 | Historical pattern learned from approved pre-delivery features |
| 8 | `categorical__customer_city_mercedes` | 2.472610 | Historical pattern learned from approved pre-delivery features |
| 9 | `categorical__customer_city_vila pereira` | 2.471482 | Historical pattern learned from approved pre-delivery features |
| 10 | `categorical__customer_city_porteirinha` | 2.445965 | Historical pattern learned from approved pre-delivery features |

## SHAP Status

SHAP was not run because the optional `shap` package is not installed.

## Example High-Risk Explanation

A high-risk order may be flagged because it combines signals such as a cross-state route, high freight value, long estimated delivery window, heavier shipment, or a historically riskier destination/product pattern.
