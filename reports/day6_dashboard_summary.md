# Day 6 Dashboard Summary

## Summary

The final model now generates order-level SLA breach risk scores and business risk buckets. The dashboard file is available at `dashboard/app.py` and reads from `data/predictions/delivery_risk_scores.csv`.

## Risk Score Output

- Output file: `data/predictions/delivery_risk_scores.csv`
- Rows scored: 96,470
- Columns: `order_id`, `sla_breach_probability`, `risk_bucket`, `customer_state`, `seller_state`, `product_category_name`, `estimated_delivery_days`, `top_risk_reason`
- Actual SLA breach rate in the scored dataset: 8.11%

## Risk Bucket Distribution

| Risk Bucket | Orders |
| --- | ---: |
| Low | 33,419 |
| Medium | 47,760 |
| High | 13,908 |
| Critical | 1,383 |

## Business Explanation

- Low risk orders have predicted SLA breach probability up to 0.30 and need no immediate action.
- Medium risk orders have probability above 0.30 and up to 0.60 and should be monitored.
- High risk orders have probability above 0.60 and up to 0.80 and should be prioritized.
- Critical risk orders have probability above 0.80 and should receive immediate intervention.

## Highest Average Risk Segments

Top customer states by average predicted risk:

| Customer State | Average Risk |
| --- | ---: |
| AL | 0.6172 |
| BA | 0.5364 |
| RJ | 0.5333 |
| CE | 0.5289 |
| MA | 0.5275 |

Top seller states by average predicted risk:

| Seller State | Average Risk |
| --- | ---: |
| MA | 0.5354 |
| SP | 0.4172 |
| RJ | 0.3983 |
| PI | 0.3817 |
| AM | 0.3739 |

Top product categories by average predicted risk:

| Product Category | Average Risk |
| --- | ---: |
| pc_gamer | 0.5776 |
| portateis_cozinha_e_preparadores_de_alimentos | 0.5066 |
| casa_conforto_2 | 0.4970 |
| artes_e_artesanato | 0.4941 |
| moveis_colchao_e_estofado | 0.4739 |

## Dashboard Usage

Run the dashboard locally with:

```bash
streamlit run dashboard/app.py
```

The dashboard includes total orders scored, actual SLA breach rate, risk bucket counts, high-risk order table, probability distribution, and risk charts by customer state, seller state, and product category.
