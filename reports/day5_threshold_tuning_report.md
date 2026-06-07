# Day 5 Threshold Tuning Report

Thresholds are evaluated from 0.05 to 0.95 for the SLA breach class.
The operational recommendation in the optimization report uses recall-first ranking with basic precision and false-positive guardrails.

| Model | Threshold | Precision Class 1 | Recall Class 1 | F1 Class 1 | PR-AUC | ROC-AUC | False Positives | False Negatives | True Positives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Optimized Logistic Regression | 0.0500 | 0.0842 | 0.9923 | 0.1552 | 0.1899 | 0.7084 | 16891 | 12 | 1553 |
| Optimized Logistic Regression | 0.1000 | 0.0895 | 0.9725 | 0.1638 | 0.1899 | 0.7084 | 15492 | 43 | 1522 |
| Optimized Logistic Regression | 0.1500 | 0.0958 | 0.9342 | 0.1738 | 0.1899 | 0.7084 | 13798 | 103 | 1462 |
| Optimized Logistic Regression | 0.2000 | 0.1020 | 0.8843 | 0.1829 | 0.1899 | 0.7084 | 12188 | 181 | 1384 |
| Optimized Logistic Regression | 0.2500 | 0.1098 | 0.8339 | 0.1941 | 0.1899 | 0.7084 | 10579 | 260 | 1305 |
| Optimized Logistic Regression | 0.3000 | 0.1196 | 0.7827 | 0.2075 | 0.1899 | 0.7084 | 9019 | 340 | 1225 |
| Optimized Logistic Regression | 0.3500 | 0.1280 | 0.7157 | 0.2171 | 0.1899 | 0.7084 | 7631 | 445 | 1120 |
| Optimized Logistic Regression | 0.4000 | 0.1387 | 0.6588 | 0.2292 | 0.1899 | 0.7084 | 6400 | 534 | 1031 |
| Optimized Logistic Regression | 0.4500 | 0.1508 | 0.5949 | 0.2406 | 0.1899 | 0.7084 | 5242 | 634 | 931 |
| Optimized Logistic Regression | 0.5000 | 0.1676 | 0.5457 | 0.2564 | 0.1899 | 0.7084 | 4242 | 711 | 854 |
| Optimized Logistic Regression | 0.5500 | 0.1832 | 0.4831 | 0.2656 | 0.1899 | 0.7084 | 3371 | 809 | 756 |
| Optimized Logistic Regression | 0.6000 | 0.2022 | 0.4147 | 0.2719 | 0.1899 | 0.7084 | 2560 | 916 | 649 |
| Optimized Logistic Regression | 0.6500 | 0.2178 | 0.3412 | 0.2659 | 0.1899 | 0.7084 | 1918 | 1031 | 534 |
| Optimized Logistic Regression | 0.7000 | 0.2387 | 0.2696 | 0.2532 | 0.1899 | 0.7084 | 1346 | 1143 | 422 |
| Optimized Logistic Regression | 0.7500 | 0.2630 | 0.2006 | 0.2276 | 0.1899 | 0.7084 | 880 | 1251 | 314 |
| Optimized Logistic Regression | 0.8000 | 0.2821 | 0.1291 | 0.1771 | 0.1899 | 0.7084 | 514 | 1363 | 202 |
| Optimized Logistic Regression | 0.8500 | 0.3055 | 0.0677 | 0.1109 | 0.1899 | 0.7084 | 241 | 1459 | 106 |
| Optimized Logistic Regression | 0.9000 | 0.3804 | 0.0224 | 0.0422 | 0.1899 | 0.7084 | 57 | 1530 | 35 |
| Optimized Logistic Regression | 0.9500 | 0.3846 | 0.0032 | 0.0063 | 0.1899 | 0.7084 | 8 | 1560 | 5 |
| Optimized Random Forest | 0.0500 | 0.0811 | 1.0000 | 0.1501 | 0.1640 | 0.6786 | 17729 | 0 | 1565 |
| Optimized Random Forest | 0.1000 | 0.0811 | 1.0000 | 0.1501 | 0.1640 | 0.6786 | 17729 | 0 | 1565 |
| Optimized Random Forest | 0.1500 | 0.0811 | 1.0000 | 0.1501 | 0.1640 | 0.6786 | 17729 | 0 | 1565 |
| Optimized Random Forest | 0.2000 | 0.0811 | 1.0000 | 0.1501 | 0.1640 | 0.6786 | 17729 | 0 | 1565 |
| Optimized Random Forest | 0.2500 | 0.0811 | 1.0000 | 0.1501 | 0.1640 | 0.6786 | 17729 | 0 | 1565 |
| Optimized Random Forest | 0.3000 | 0.0811 | 1.0000 | 0.1501 | 0.1640 | 0.6786 | 17729 | 0 | 1565 |
| Optimized Random Forest | 0.3500 | 0.0811 | 1.0000 | 0.1501 | 0.1640 | 0.6786 | 17729 | 0 | 1565 |
| Optimized Random Forest | 0.4000 | 0.0816 | 0.9994 | 0.1508 | 0.1640 | 0.6786 | 17612 | 1 | 1564 |
| Optimized Random Forest | 0.4500 | 0.0877 | 0.9623 | 0.1608 | 0.1640 | 0.6786 | 15661 | 59 | 1506 |
| Optimized Random Forest | 0.5000 | 0.1339 | 0.6460 | 0.2219 | 0.1640 | 0.6786 | 6537 | 554 | 1011 |
| Optimized Random Forest | 0.5500 | 0.2549 | 0.1259 | 0.1685 | 0.1640 | 0.6786 | 576 | 1368 | 197 |
| Optimized Random Forest | 0.6000 | 0.0000 | 0.0000 | 0.0000 | 0.1640 | 0.6786 | 0 | 1565 | 0 |
| Optimized Random Forest | 0.6500 | 0.0000 | 0.0000 | 0.0000 | 0.1640 | 0.6786 | 0 | 1565 | 0 |
| Optimized Random Forest | 0.7000 | 0.0000 | 0.0000 | 0.0000 | 0.1640 | 0.6786 | 0 | 1565 | 0 |
| Optimized Random Forest | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.1640 | 0.6786 | 0 | 1565 | 0 |
| Optimized Random Forest | 0.8000 | 0.0000 | 0.0000 | 0.0000 | 0.1640 | 0.6786 | 0 | 1565 | 0 |
| Optimized Random Forest | 0.8500 | 0.0000 | 0.0000 | 0.0000 | 0.1640 | 0.6786 | 0 | 1565 | 0 |
| Optimized Random Forest | 0.9000 | 0.0000 | 0.0000 | 0.0000 | 0.1640 | 0.6786 | 0 | 1565 | 0 |
| Optimized Random Forest | 0.9500 | 0.0000 | 0.0000 | 0.0000 | 0.1640 | 0.6786 | 0 | 1565 | 0 |
| HistGradientBoosting | 0.0500 | 0.1088 | 0.8754 | 0.1935 | 0.2078 | 0.7200 | 11224 | 195 | 1370 |
| HistGradientBoosting | 0.1000 | 0.1665 | 0.5406 | 0.2546 | 0.2078 | 0.7200 | 4235 | 719 | 846 |
| HistGradientBoosting | 0.1500 | 0.2316 | 0.3335 | 0.2734 | 0.2078 | 0.7200 | 1732 | 1043 | 522 |
| HistGradientBoosting | 0.2000 | 0.2841 | 0.1968 | 0.2325 | 0.2078 | 0.7200 | 776 | 1257 | 308 |
| HistGradientBoosting | 0.2500 | 0.3445 | 0.1118 | 0.1688 | 0.2078 | 0.7200 | 333 | 1390 | 175 |
| HistGradientBoosting | 0.3000 | 0.4142 | 0.0633 | 0.1098 | 0.2078 | 0.7200 | 140 | 1466 | 99 |
| HistGradientBoosting | 0.3500 | 0.4310 | 0.0319 | 0.0595 | 0.2078 | 0.7200 | 66 | 1515 | 50 |
| HistGradientBoosting | 0.4000 | 0.4630 | 0.0160 | 0.0309 | 0.2078 | 0.7200 | 29 | 1540 | 25 |
| HistGradientBoosting | 0.4500 | 0.5217 | 0.0077 | 0.0151 | 0.2078 | 0.7200 | 11 | 1553 | 12 |
| HistGradientBoosting | 0.5000 | 0.6000 | 0.0019 | 0.0038 | 0.2078 | 0.7200 | 2 | 1562 | 3 |
| HistGradientBoosting | 0.5500 | 0.3333 | 0.0006 | 0.0013 | 0.2078 | 0.7200 | 2 | 1564 | 1 |
| HistGradientBoosting | 0.6000 | 0.0000 | 0.0000 | 0.0000 | 0.2078 | 0.7200 | 0 | 1565 | 0 |
| HistGradientBoosting | 0.6500 | 0.0000 | 0.0000 | 0.0000 | 0.2078 | 0.7200 | 0 | 1565 | 0 |
| HistGradientBoosting | 0.7000 | 0.0000 | 0.0000 | 0.0000 | 0.2078 | 0.7200 | 0 | 1565 | 0 |
| HistGradientBoosting | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.2078 | 0.7200 | 0 | 1565 | 0 |
| HistGradientBoosting | 0.8000 | 0.0000 | 0.0000 | 0.0000 | 0.2078 | 0.7200 | 0 | 1565 | 0 |
| HistGradientBoosting | 0.8500 | 0.0000 | 0.0000 | 0.0000 | 0.2078 | 0.7200 | 0 | 1565 | 0 |
| HistGradientBoosting | 0.9000 | 0.0000 | 0.0000 | 0.0000 | 0.2078 | 0.7200 | 0 | 1565 | 0 |
| HistGradientBoosting | 0.9500 | 0.0000 | 0.0000 | 0.0000 | 0.2078 | 0.7200 | 0 | 1565 | 0 |
