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
| Low | 34,891 |
| Medium | 41,184 |
| High | 16,412 |
| Critical | 3,983 |

## Business Explanation

- Low risk orders have predicted SLA breach probability up to 0.30 and need no immediate action.
- Medium risk orders have probability above 0.30 and up to 0.60 and should be monitored.
- High risk orders have probability above 0.60 and up to 0.80 and should be prioritized.
- Critical risk orders have probability above 0.80 and should receive immediate intervention.

## Highest Average Risk Segments

Top customer states by average predicted risk:

| Customer State | Average Risk |
| --- | ---: |
| AL | 0.6748 |
| MA | 0.5909 |
| SE | 0.5829 |
| RR | 0.5806 |
| CE | 0.5685 |

Top seller states by average predicted risk:

| Seller State | Average Risk |
| --- | ---: |
| MA | 0.6827 |
| AM | 0.6679 |
| RN | 0.4433 |
| CE | 0.4281 |
| RJ | 0.4271 |

Top product categories by average predicted risk:

| Product Category | Average Risk |
| --- | ---: |
| fashion_esporte | 0.5329 |
| casa_conforto_2 | 0.5321 |
| moveis_colchao_e_estofado | 0.5292 |
| fashion_underwear_e_moda_praia | 0.4952 |
| alimentos | 0.4939 |

## Dashboard Usage

Run the dashboard locally with:

```bash
streamlit run dashboard/app.py
```

The dashboard includes total orders scored, actual SLA breach rate, risk bucket counts, high-risk order table, probability distribution, and risk charts by customer state, seller state, and product category.
