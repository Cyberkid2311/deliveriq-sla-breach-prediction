# Data Dictionary

## 1. olist_customers_dataset.csv

### Description
Contains customer identification and location information.

### Summary
- Number of Rows: 99,441
- Number of Columns: 5

### Columns
| Column Name | Description |
|------------|-------------|
| customer_id | Unique identifier for each customer order record |
| customer_unique_id | Unique identifier representing the actual customer |
| customer_zip_code_prefix | Customer ZIP code prefix |
| customer_city | Customer city |
| customer_state | Customer state |


---

## 2. olist_geolocation_dataset.csv

### Description
Contains geographic location information based on ZIP code regions.

### Summary
- Number of Rows: 1,000,163
- Number of Columns: 5

### Columns
| Column Name | Description |
|------------|-------------|
| geolocation_zip_code_prefix | ZIP code prefix |
| geolocation_lat | Latitude coordinate |
| geolocation_lng | Longitude coordinate |
| geolocation_city | City name |
| geolocation_state | State name |


---

## 3. olist_order_items_dataset.csv

### Description
Contains item-level details for each order.

### Summary
- Number of Rows: 112,650
- Number of Columns: 7

### Columns
| Column Name | Description |
|------------|-------------|
| order_id | Unique order identifier |
| order_item_id | Identifier of item within order |
| product_id | Product identifier |
| seller_id | Seller identifier |
| shipping_limit_date | Deadline for shipment |
| price | Product price |
| freight_value | Shipping cost |


---

## 4. olist_orders_dataset.csv

### Description
Contains order lifecycle information and delivery timeline.

### Summary
- Number of Rows: 99,441
- Number of Columns: 8

### Columns
| Column Name | Description |
|------------|-------------|
| order_id | Unique order identifier |
| customer_id | Customer identifier |
| order_status | Current order status |
| order_purchase_timestamp | Purchase timestamp |
| order_approved_at | Order approval timestamp |
| order_delivered_carrier_date | Date delivered to carrier |
| order_delivered_customer_date | Date delivered to customer |
| order_estimated_delivery_date | Estimated delivery date |


---

## 5. olist_products_dataset.csv

### Description
Contains product metadata and physical characteristics.

### Summary
- Number of Rows: 32,951
- Number of Columns: 9

### Columns
| Column Name | Description |
|------------|-------------|
| product_id | Product identifier |
| product_category_name | Product category |
| product_name_lenght | Product name length |
| product_description_lenght | Product description length |
| product_photos_qty | Number of product photos |
| product_weight_g | Product weight in grams |
| product_length_cm | Product length in centimeters |
| product_height_cm | Product height in centimeters |
| product_width_cm | Product width in centimeters |


---

## 6. olist_sellers_dataset.csv

### Description
Contains seller identification and location information.

### Summary
- Number of Rows: 3,095
- Number of Columns: 4

### Columns
| Column Name | Description |
|------------|-------------|
| seller_id | Seller identifier |
| seller_zip_code_prefix | Seller ZIP code prefix |
| seller_city | Seller city |
| seller_state | Seller state |