from pathlib import Path

import pandas as pd


ORDER_DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

ORDER_ITEM_NUMERIC_COLUMNS = [
    "order_item_id",
    "price",
    "freight_value",
]

PRODUCT_NUMERIC_COLUMNS = [
    "product_name_length",
    "product_description_length",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]

BASE_ORDER_COLUMNS = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",
    "item_count",
    "product_count",
    "seller_count",
    "product_category_count",
    "primary_product_id",
    "primary_product_category_name",
    "primary_seller_id",
    "primary_seller_zip_code_prefix",
    "primary_seller_city",
    "primary_seller_state",
    "total_price",
    "avg_price",
    "total_freight_value",
    "avg_freight_value",
    "avg_product_weight_g",
    "avg_product_length_cm",
    "avg_product_height_cm",
    "avg_product_width_cm",
    "avg_product_volume_cm3",
]


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to lower snake case."""
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    return df


def clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim leading/trailing whitespace from text columns."""
    df = df.copy()
    string_columns = df.select_dtypes(include=["object", "string"]).columns

    for column in string_columns:
        df[column] = df[column].astype("string").str.strip()

    return df


def clean_basic_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply low-risk reusable cleaning to a dataframe."""
    df = clean_column_names(df)
    df = clean_string_columns(df)
    return df.drop_duplicates()


def clean_zip_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Keep Olist zip prefixes as five-character strings."""
    df = df.copy()

    if column_name in df.columns:
        df[column_name] = (
            df[column_name]
            .astype("string")
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
            .str.zfill(5)
        )

    return df


def parse_datetime_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Parse date/time columns, coercing invalid values to missing."""
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def parse_numeric_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Parse numeric columns, coercing invalid values to missing."""
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Clean the main orders table."""
    orders = clean_basic_dataframe(orders)
    orders = parse_datetime_columns(orders, ORDER_DATE_COLUMNS)
    orders = orders.drop_duplicates(subset=["order_id"], keep="last")

    if "order_status" in orders.columns:
        orders["order_status"] = orders["order_status"].str.lower()

    return orders


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """Clean customer location fields."""
    customers = clean_basic_dataframe(customers)
    customers = clean_zip_column(customers, "customer_zip_code_prefix")
    customers = customers.drop_duplicates(subset=["customer_id"], keep="last")

    if "customer_city" in customers.columns:
        customers["customer_city"] = customers["customer_city"].str.lower()

    if "customer_state" in customers.columns:
        customers["customer_state"] = customers["customer_state"].str.upper()

    return customers


def clean_order_items(order_items: pd.DataFrame) -> pd.DataFrame:
    """Clean product/order-item detail rows."""
    order_items = clean_basic_dataframe(order_items)
    order_items = parse_datetime_columns(order_items, ["shipping_limit_date"])
    order_items = parse_numeric_columns(order_items, ORDER_ITEM_NUMERIC_COLUMNS)
    return order_items.drop_duplicates(
        subset=["order_id", "order_item_id"],
        keep="last",
    )


def clean_sellers(sellers: pd.DataFrame) -> pd.DataFrame:
    """Clean seller location fields."""
    sellers = clean_basic_dataframe(sellers)
    sellers = clean_zip_column(sellers, "seller_zip_code_prefix")
    sellers = sellers.drop_duplicates(subset=["seller_id"], keep="last")

    if "seller_city" in sellers.columns:
        sellers["seller_city"] = sellers["seller_city"].str.lower()

    if "seller_state" in sellers.columns:
        sellers["seller_state"] = sellers["seller_state"].str.upper()

    return sellers


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    """Clean product attributes."""
    products = clean_basic_dataframe(products)
    products = products.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        }
    )
    products = parse_numeric_columns(products, PRODUCT_NUMERIC_COLUMNS)
    products = products.drop_duplicates(subset=["product_id"], keep="last")

    if "product_category_name" in products.columns:
        products["product_category_name"] = (
            products["product_category_name"].str.lower().fillna("unknown")
        )

    products["product_volume_cm3"] = (
        products["product_length_cm"]
        * products["product_height_cm"]
        * products["product_width_cm"]
    )

    return products


def clean_olist_tables(raw_dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Clean the minimum Olist tables required for the base order dataset."""
    return {
        "orders": clean_orders(raw_dataframes["orders"]),
        "customers": clean_customers(raw_dataframes["customers"]),
        "order_items": clean_order_items(raw_dataframes["order_items"]),
        "sellers": clean_sellers(raw_dataframes["sellers"]),
        "products": clean_products(raw_dataframes["products"]),
    }


def aggregate_order_items_to_order_level(
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    sellers: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate item-level product/seller rows to one row per order before joining.
    """
    item_details = (
        order_items.merge(
            products,
            on="product_id",
            how="left",
            validate="many_to_one",
        )
        .merge(
            sellers,
            on="seller_id",
            how="left",
            validate="many_to_one",
        )
    )

    aggregated = (
        item_details.groupby("order_id", as_index=False)
        .agg(
            item_count=("order_item_id", "count"),
            product_count=("product_id", "nunique"),
            seller_count=("seller_id", "nunique"),
            product_category_count=("product_category_name", "nunique"),
            primary_product_id=("product_id", "first"),
            primary_product_category_name=("product_category_name", "first"),
            primary_seller_id=("seller_id", "first"),
            primary_seller_zip_code_prefix=("seller_zip_code_prefix", "first"),
            primary_seller_city=("seller_city", "first"),
            primary_seller_state=("seller_state", "first"),
            total_price=("price", "sum"),
            avg_price=("price", "mean"),
            total_freight_value=("freight_value", "sum"),
            avg_freight_value=("freight_value", "mean"),
            avg_product_weight_g=("product_weight_g", "mean"),
            avg_product_length_cm=("product_length_cm", "mean"),
            avg_product_height_cm=("product_height_cm", "mean"),
            avg_product_width_cm=("product_width_cm", "mean"),
            avg_product_volume_cm3=("product_volume_cm3", "mean"),
        )
    )

    if aggregated["order_id"].duplicated().any():
        raise ValueError("Order-item aggregation produced duplicate order_id values.")

    return aggregated


def build_base_order_dataset(clean_dataframes: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Build the first clean modeling table with one row per order.

    Your first responsibility is to create the first clean, order-level dataset.
    The final ML model should have one row per order. Be careful when joining
    order items because one order can have multiple products. First, aggregate
    item-level data, then join it with the order table.
    """
    orders = clean_dataframes["orders"]
    customers = clean_dataframes["customers"]
    order_items = clean_dataframes["order_items"]
    sellers = clean_dataframes["sellers"]
    products = clean_dataframes["products"]

    item_features = aggregate_order_items_to_order_level(
        order_items=order_items,
        products=products,
        sellers=sellers,
    )

    base_orders = (
        orders.merge(
            customers,
            on="customer_id",
            how="left",
            validate="many_to_one",
        )
        .merge(
            item_features,
            on="order_id",
            how="left",
            validate="one_to_one",
        )
    )

    count_columns = [
        "item_count",
        "product_count",
        "seller_count",
        "product_category_count",
    ]
    total_columns = [
        "total_price",
        "total_freight_value",
    ]
    base_orders[count_columns] = base_orders[count_columns].fillna(0).astype("int64")
    base_orders[total_columns] = base_orders[total_columns].fillna(0)

    if base_orders["order_id"].duplicated().any():
        duplicate_count = int(base_orders["order_id"].duplicated().sum())
        raise ValueError(f"Base dataset is not order-level: {duplicate_count} duplicate rows.")

    missing_columns = [
        column for column in BASE_ORDER_COLUMNS if column not in base_orders.columns
    ]
    if missing_columns:
        raise ValueError("Missing base dataset columns:\n" + "\n".join(missing_columns))

    return base_orders[BASE_ORDER_COLUMNS].sort_values("order_id").reset_index(drop=True)


def save_base_order_dataset(
    base_orders: pd.DataFrame,
    output_path: str | Path = "data/processed/base_order_dataset.csv",
) -> None:
    """Save the base order-level dataset."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    base_orders.to_csv(output_path, index=False)
