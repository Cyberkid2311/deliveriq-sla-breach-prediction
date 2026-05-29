# Day 3 – Feature Engineering Analysis Summary

## Objective

The objective of this analysis was to evaluate the relationship between various features and the target variable, `sla_breached`, in order to identify features that may be useful for predicting SLA breaches in future machine learning models.

Unlike traditional exploratory data analysis, this stage focuses on determining whether specific variables contain predictive information that can help distinguish between orders that meet their delivery commitments and those that breach their Service Level Agreement (SLA).

**Dataset Used:** `data/processed/modeling_dataset_v1.csv`

**Dataset Shape:**

* Rows: 96,470
* Columns: 38

**Target Variable:**

* `sla_breached`

  * 1 = SLA Breached
  * 0 = SLA Met

---

# Features Analyzed

The following features were analyzed against the target variable:

1. Customer State
2. Seller State
3. Purchase Day of Week
4. Weekend vs Weekday Orders
5. Product Category
6. Product Weight Buckets
7. Freight Value Buckets

For each feature, the SLA breach rate was calculated and compared across different groups to determine whether meaningful differences existed.

---

# 1. Customer State Analysis

SLA breach rates were calculated for each customer state to evaluate whether customer location influences delivery performance.

### Key Findings

| Customer State | Breach Rate (%) |
| -------------- | --------------: |
| Alagoas        |           23.93 |
| Maranhão       |           19.67 |
| Piauí          |           15.97 |
| Ceará          |           15.32 |
| Sergipe        |           15.22 |

The analysis revealed substantial variation in breach rates across customer locations. States such as Alagoas, Maranhão, and Piauí exhibited significantly higher breach rates than many other regions.

These findings suggest that customer location may contain valuable predictive information and could serve as an important feature during model development.

---

# 2. Seller State Analysis

SLA breach rates were analyzed based on seller location to determine whether the origin of an order influences delivery performance.

### Key Findings

| Seller State        | Breach Rate (%) |
| ------------------- | --------------: |
| Amazonas            |          66.67* |
| Maranhão            |           23.20 |
| Pará                |           12.50 |
| Rio Grande do Norte |            9.80 |
| Ceará               |            9.41 |

*The Amazonas result was based on only three orders and should therefore be interpreted with caution.

The analysis showed noticeable variation across seller states. Although some extreme values were influenced by small sample sizes, the overall pattern suggests that seller location may contribute useful predictive information regarding SLA breach risk.

---

# 3. Purchase Day of Week Analysis

Orders were grouped according to the day of the week on which they were placed.

### Key Findings

| Day       | Breach Rate (%) |
| --------- | --------------: |
| Monday    |            9.05 |
| Tuesday   |            8.49 |
| Friday    |            8.45 |
| Wednesday |            7.80 |
| Saturday  |            7.60 |
| Thursday  |            7.57 |
| Sunday    |            7.49 |

Orders placed on Monday experienced the highest breach rate, while orders placed on Sunday experienced the lowest.

However, the overall variation between days was relatively small, indicating that purchase day may provide only limited predictive value compared with other features analyzed in this study.

---

# 4. Weekend vs Weekday Analysis

Orders were grouped into weekday and weekend categories to determine whether purchasing behavior during weekends influences delivery performance.

### Key Findings

| Order Type | Breach Rate (%) |
| ---------- | --------------: |
| Weekday    |            8.28 |
| Weekend    |            7.54 |

The difference between weekday and weekend orders was less than one percentage point.

This suggests that whether an order was placed on a weekend or a weekday is unlikely to be a strong predictor of SLA breach outcomes.

---

# 5. Product Category Analysis

The ten most common product categories in the dataset were analyzed to determine whether product type influences delivery performance.

### Key Findings

| Product Category         | Breach Rate (%) |
| ------------------------ | --------------: |
| Beauty and Health        |            8.99 |
| Bed, Bath and Table      |            8.85 |
| Automotive               |            8.65 |
| Furniture and Decoration |            8.56 |
| Watches and Gifts        |            8.56 |
| Telephony                |            8.54 |
| Sports and Leisure       |            7.80 |
| Computer Accessories     |            7.74 |
| Toys                     |            7.52 |
| Household Utilities      |            7.00 |

The analysis revealed measurable variation across product categories.

Beauty and health products, bedding-related products, and automotive products exhibited higher breach rates, while household utility products recorded the lowest breach rate among the major categories analyzed.

These findings indicate that product category may provide useful predictive information for SLA breach prediction.

---

# 6. Product Weight Bucket Analysis

Products were grouped into weight ranges to evaluate whether product weight affects delivery performance.

### Key Findings

| Weight Bucket | Breach Rate (%) |
| ------------- | --------------: |
| 5000g+        |            9.18 |
| 2000g–5000g   |            8.53 |
| 1000g–2000g   |            8.40 |
| 0g–500g       |            7.75 |
| 500g–1000g    |            7.71 |

A clear trend was observed in which heavier products generally experienced higher SLA breach rates.

The heaviest products recorded the highest breach rates, while lighter products exhibited lower breach rates.

This suggests that product weight may be a meaningful predictor of delivery performance.

---

# 7. Freight Value Bucket Analysis

Orders were grouped according to freight value to determine whether shipping cost is associated with SLA breach risk.

### Key Findings

| Freight Value Bucket | Breach Rate (%) |
| -------------------- | --------------: |
| 50+                  |            9.90 |
| 30–50                |            9.25 |
| 20–30                |            9.06 |
| 10–20                |            7.78 |
| 0–10                 |            6.22 |

A strong positive relationship was observed between freight value and SLA breach rate.

Orders with the highest freight values consistently exhibited the highest breach rates, while orders with the lowest freight values experienced the lowest breach rates.

Among all features analyzed, freight value demonstrated one of the clearest relationships with SLA breach behavior.

---

# Top 5 Patterns Identified

## 1. Customer State Significantly Influences SLA Breach Rates

Customer location showed substantial variation in breach rates, indicating that geographic factors may influence delivery outcomes and provide valuable predictive information.

## 2. Freight Value Has a Strong Positive Relationship with SLA Breaches

As freight value increased, breach rates increased consistently. This was one of the strongest patterns identified during the analysis.

## 3. Seller State Appears to Affect Delivery Performance

Seller location demonstrated noticeable differences in breach rates, suggesting that the origin of shipments may contribute to delivery risk.

## 4. Heavier Products Tend to Experience More Delivery Delays

Higher product weights were associated with increased SLA breach rates, indicating that shipment characteristics influence delivery performance.

## 5. Product Category Contains Useful Predictive Information

Different product categories exhibited different breach behaviors, suggesting that product-specific logistics challenges may affect delivery outcomes.

---

# Preliminary Feature Assessment

Based on the analyses conducted, the following features appear most promising for predictive modeling:

1. Customer State
2. Freight Value
3. Seller State
4. Product Weight
5. Product Category

Features that appear comparatively weaker include:

* Purchase Day of Week
* Weekend vs Weekday Indicator

These observations are based on exploratory analysis and will require further validation during feature engineering and model training.

---

# Conclusion

This feature engineering analysis identified several variables that exhibit meaningful relationships with SLA breach behavior. Location-based features, freight-related features, product characteristics, and product categories demonstrated the strongest predictive potential.

The insights generated during this analysis will be used to guide feature selection, feature engineering, and model development in the subsequent stages of the SLA breach prediction project.
