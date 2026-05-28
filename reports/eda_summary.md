# Exploratory Data Analysis (EDA) Summary

## Overview

This report summarizes the exploratory data analysis performed on the Olist ecommerce delivery dataset to identify patterns related to SLA (Service Level Agreement) breaches and delivery delays.

The analysis focused on:

* Delivery-related timestamps
* Order status distribution
* SLA breach patterns
* Regional delivery performance
* Product category delays
* Distance-based delivery behavior

---

# Dataset Summary

The processed dataset used for analysis:

```text
data/gold/olist_final_consumption_dataset.csv
```

Dataset dimensions:

* Total Records: 112,650
* Total Columns: 43

The dataset contains customer, seller, product, delivery, and logistics-related features.

---

# SLA-Related Column Analysis

The following SLA-related columns were analyzed:

* `order_purchase_timestamp`
* `order_estimated_delivery_date`
* `order_delivered_customer_date`
* `order_status`

## Missing Value Findings

| Column                        | Missing Values |
| ----------------------------- | -------------- |
| order_purchase_timestamp      | 0              |
| order_estimated_delivery_date | 0              |
| order_delivered_customer_date | 2,454          |
| order_status                  | 0              |

### Observation

The `order_delivered_customer_date` column contained 2,454 missing values. These missing records are likely associated with canceled, unavailable, or undelivered orders.

All orders contained estimated delivery dates, which allowed SLA analysis to be performed consistently.

---

# Basic Delivery Analysis

## Order Status Distribution

| Order Status | Count   |
| ------------ | ------- |
| Delivered    | 110,197 |
| Shipped      | 1,185   |
| Canceled     | 542     |
| Invoiced     | 359     |
| Processing   | 357     |
| Unavailable  | 7       |
| Approved     | 3       |

### Observation

Most orders in the dataset were successfully delivered. Only a small portion of orders were canceled, unavailable, or still in processing/shipping states.

---

# SLA Breach Analysis

The dataset already contained a precomputed `sla_breached` column:

* `0` → Delivered within SLA
* `1` → Delivered after promised date

## Overall SLA Breach Rate

| SLA Status   | Count   |
| ------------ | ------- |
| Not Breached | 103,935 |
| Breached     | 8,715   |

Overall SLA breach rate:

```text
7.74%
```

### Observation

Approximately 7.74% of orders were delivered later than the promised delivery date.

---

# SLA Breach by Customer State

Top customer states with highest SLA breach rates:

| Customer State | SLA Breach Rate |
| -------------- | --------------- |
| AL             | 23.20%          |
| MA             | 19.78%          |
| SE             | 15.84%          |
| PI             | 14.94%          |
| CE             | 14.75%          |

### Observation

Certain customer regions experienced significantly higher delivery delays compared to the overall average breach rate.

---

# SLA Breach by Seller State

Top seller states with highest SLA breach rates:

| Seller State | SLA Breach Rate |
| ------------ | --------------- |
| AM           | 66.67%          |
| MA           | 23.46%          |
| PA           | 12.50%          |
| RN           | 10.71%          |
| CE           | 8.51%           |

### Observation

Some seller states showed noticeably higher SLA breach rates. However, certain states may contain smaller sample sizes and should be interpreted carefully.

---

# SLA Breach by Purchase Day

| Purchase Day | SLA Breach Rate |
| ------------ | --------------- |
| Monday       | 8.58%           |
| Tuesday      | 8.14%           |
| Friday       | 7.97%           |
| Wednesday    | 7.39%           |
| Sunday       | 7.36%           |
| Thursday     | 7.24%           |
| Saturday     | 7.14%           |

### Observation

Orders placed on Monday showed the highest SLA breach rate, while Saturday purchases showed the lowest breach rate.

This may indicate operational backlog or increased logistics load during the beginning of the week.

---

# SLA Breach by Product Category

Top product categories with highest SLA breach rates:

| Product Category               | SLA Breach Rate |
| ------------------------------ | --------------- |
| casa_conforto_2                | 16.67%          |
| moveis_colchao_e_estofado      | 13.16%          |
| audio                          | 12.64%          |
| fashion_underwear_e_moda_praia | 12.21%          |
| artigos_de_natal               | 11.76%          |

### Observation

Certain product categories experienced higher delivery delays than others, potentially due to handling complexity, logistics requirements, or regional demand patterns.

---

# Distance-Based SLA Analysis

The original task referenced freight value analysis. However, the processed dataset did not contain a `freight_value` column.

Instead, the following logistics-related features were available:

* `seller_customer_distance_km`
* `distance_bucket`

Distance-based analysis was used as an alternative logistics indicator.

## SLA Breach Rate by Distance Bucket

| Distance Bucket | SLA Breach Rate |
| --------------- | --------------- |
| 2000+ km        | 13.11%          |
| 1000-2000 km    | 10.42%          |
| 500-1000 km     | 8.09%           |
| 200-500 km      | 6.86%           |
| 0-50 km         | 6.45%           |
| 50-200 km       | 5.93%           |

### Observation

Longer delivery distances showed consistently higher SLA breach rates.

Orders traveling more than 2000 km experienced the highest breach rate (13.11%), indicating that delivery distance is strongly associated with late deliveries.

---

# Conclusion

Key findings from the analysis:

* Most orders were successfully delivered.
* Approximately 7.74% of orders breached SLA.
* Missing delivery dates were mainly associated with non-delivered orders.
* Certain customer and seller states experienced significantly higher delivery delays.
* Monday purchases showed slightly higher SLA breach rates.
* Some product categories had elevated delay patterns.
* Longer delivery distances strongly correlated with higher SLA breach probability.

The analysis demonstrates that geography, logistics distance, and product characteristics play important roles in delivery performance and SLA reliability.
