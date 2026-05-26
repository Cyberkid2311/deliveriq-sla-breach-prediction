import numpy as np
import pandas as pd


FINAL_GOLD_COLUMNS = [
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "purchase_dayofweek",
    "purchase_hour",
    "approval_delay_hours",
    "carrier_handover_days",
    "actual_delivery_days",
    "estimated_delivery_days",
    "delivery_delay_days",
    "sla_breached",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",
    "seller_zip_code_prefix",
    "seller_city",
    "seller_state",
    "product_category_name",
    "product_name_length",
    "product_description_length",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "product_volume_cm3",
    "product_weight_kg",
    "customer_geo_city",
    "customer_geo_state",
    "seller_geo_city",
    "seller_geo_state",
    "seller_customer_distance_km",
    "distance_bucket",
    "seller_customer_same_state",
    "seller_customer_same_city",
]


# --------------------------------------------------
# Basic Cleaning Helpers
# --------------------------------------------------

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    string_columns = df.select_dtypes(include=["object"]).columns

    for column in string_columns:
        df[column] = df[column].astype("string").str.strip()

    return df


def clean_basic_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = clean_string_columns(df)
    df = df.drop_duplicates()
    return df


def clean_zip_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
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
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def parse_numeric_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def get_mode_value(series: pd.Series):
    mode_values = series.dropna().mode()

    if mode_values.empty:
        return pd.NA

    return mode_values.iloc[0]


# --------------------------------------------------
# Distance Calculation
# --------------------------------------------------

def calculate_haversine_distance(
    lat1: pd.Series,
    lon1: pd.Series,
    lat2: pd.Series,
    lon2: pd.Series,
) -> pd.Series:
    """
    Calculates straight-line distance between two latitude/longitude points in KM.
    """

    earth_radius_km = 6371

    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    lat_diff = lat2_rad - lat1_rad
    lon_diff = lon2_rad - lon1_rad

    a = (
        np.sin(lat_diff / 2) ** 2
        + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(lon_diff / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))

    return earth_radius_km * c


# --------------------------------------------------
# Silver Layer Processing
# --------------------------------------------------

def process_to_silver(raw_dataframes: dict) -> dict:
    orders = clean_basic_dataframe(raw_dataframes["orders"])
    customers = clean_basic_dataframe(raw_dataframes["customers"])
    order_items = clean_basic_dataframe(raw_dataframes["order_items"])
    sellers = clean_basic_dataframe(raw_dataframes["sellers"])
    products = clean_basic_dataframe(raw_dataframes["products"])
    geolocation = clean_basic_dataframe(raw_dataframes["geolocation"])

    orders = parse_datetime_columns(
        orders,
        [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    order_items = parse_datetime_columns(
        order_items,
        ["shipping_limit_date"],
    )

    order_items = parse_numeric_columns(
        order_items,
        [
            "order_item_id",
            "price",
            "freight_value",
        ],
    )

    products = parse_numeric_columns(
        products,
        [
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ],
    )

    products = products.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        }
    )

    geolocation = parse_numeric_columns(
        geolocation,
        [
            "geolocation_lat",
            "geolocation_lng",
        ],
    )

    customers = clean_zip_column(customers, "customer_zip_code_prefix")
    sellers = clean_zip_column(sellers, "seller_zip_code_prefix")
    geolocation = clean_zip_column(geolocation, "geolocation_zip_code_prefix")

    orders = orders.drop_duplicates(subset=["order_id"], keep="last")
    customers = customers.drop_duplicates(subset=["customer_id"], keep="last")
    sellers = sellers.drop_duplicates(subset=["seller_id"], keep="last")
    products = products.drop_duplicates(subset=["product_id"], keep="last")

    order_items = order_items.drop_duplicates(
        subset=["order_id", "order_item_id"],
        keep="last",
    )

    if "order_status" in orders.columns:
        orders["order_status"] = orders["order_status"].str.lower()

    if "customer_city" in customers.columns:
        customers["customer_city"] = customers["customer_city"].str.lower()

    if "customer_state" in customers.columns:
        customers["customer_state"] = customers["customer_state"].str.upper()

    if "seller_city" in sellers.columns:
        sellers["seller_city"] = sellers["seller_city"].str.lower()

    if "seller_state" in sellers.columns:
        sellers["seller_state"] = sellers["seller_state"].str.upper()

    if "product_category_name" in products.columns:
        products["product_category_name"] = (
            products["product_category_name"]
            .str.lower()
            .fillna("unknown")
        )

    if "geolocation_city" in geolocation.columns:
        geolocation["geolocation_city"] = geolocation["geolocation_city"].str.lower()

    if "geolocation_state" in geolocation.columns:
        geolocation["geolocation_state"] = geolocation["geolocation_state"].str.upper()

    geolocation = (
        geolocation
        .groupby("geolocation_zip_code_prefix", as_index=False)
        .agg(
            geolocation_lat=("geolocation_lat", "mean"),
            geolocation_lng=("geolocation_lng", "mean"),
            geolocation_city=("geolocation_city", get_mode_value),
            geolocation_state=("geolocation_state", get_mode_value),
        )
    )

    return {
        "orders": orders,
        "customers": customers,
        "order_items": order_items,
        "sellers": sellers,
        "products": products,
        "geolocation": geolocation,
    }


# --------------------------------------------------
# Gold Layer Processing
# --------------------------------------------------

def build_final_dataset(silver_dataframes: dict) -> pd.DataFrame:
    orders = silver_dataframes["orders"].copy()
    customers = silver_dataframes["customers"].copy()
    order_items = silver_dataframes["order_items"].copy()
    sellers = silver_dataframes["sellers"].copy()
    products = silver_dataframes["products"].copy()
    geolocation = silver_dataframes["geolocation"].copy()

    products = products.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        }
    )

    # --------------------------------------------------
    # Order Features
    # --------------------------------------------------

    orders["purchase_dayofweek"] = orders["order_purchase_timestamp"].dt.dayofweek
    orders["purchase_hour"] = orders["order_purchase_timestamp"].dt.hour

    orders["approval_delay_hours"] = (
        orders["order_approved_at"] - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600

    orders["carrier_handover_days"] = (
        orders["order_delivered_carrier_date"] - orders["order_approved_at"]
    ).dt.total_seconds() / (3600 * 24)

    orders["actual_delivery_days"] = (
        orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / (3600 * 24)

    orders["estimated_delivery_days"] = (
        orders["order_estimated_delivery_date"] - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / (3600 * 24)

    orders["delivery_delay_days"] = (
        orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
    ).dt.total_seconds() / (3600 * 24)

    orders["sla_breached"] = np.where(
        (
            orders["order_delivered_customer_date"].notna()
            & orders["order_estimated_delivery_date"].notna()
            & (
                orders["order_delivered_customer_date"]
                > orders["order_estimated_delivery_date"]
            )
        ),
        1,
        0,
    )

    # --------------------------------------------------
    # Product Features
    # --------------------------------------------------

    products["product_volume_cm3"] = (
        products["product_length_cm"]
        * products["product_height_cm"]
        * products["product_width_cm"]
    )

    products["product_weight_kg"] = products["product_weight_g"] / 1000

    # --------------------------------------------------
    # Geolocation Setup
    # --------------------------------------------------

    customer_geo = geolocation.rename(
        columns={
            "geolocation_zip_code_prefix": "customer_zip_code_prefix",
            "geolocation_lat": "customer_lat",
            "geolocation_lng": "customer_lng",
            "geolocation_city": "customer_geo_city",
            "geolocation_state": "customer_geo_state",
        }
    )

    seller_geo = geolocation.rename(
        columns={
            "geolocation_zip_code_prefix": "seller_zip_code_prefix",
            "geolocation_lat": "seller_lat",
            "geolocation_lng": "seller_lng",
            "geolocation_city": "seller_geo_city",
            "geolocation_state": "seller_geo_state",
        }
    )

    # --------------------------------------------------
    # Final Dataset Join
    # Grain: one row per order item
    # --------------------------------------------------

    final_df = (
        order_items
        .merge(
            orders,
            on="order_id",
            how="left",
            validate="many_to_one",
        )
        .merge(
            customers,
            on="customer_id",
            how="left",
            validate="many_to_one",
        )
        .merge(
            sellers,
            on="seller_id",
            how="left",
            validate="many_to_one",
        )
        .merge(
            products,
            on="product_id",
            how="left",
            validate="many_to_one",
        )
        .merge(
            customer_geo,
            on="customer_zip_code_prefix",
            how="left",
            validate="many_to_one",
        )
        .merge(
            seller_geo,
            on="seller_zip_code_prefix",
            how="left",
            validate="many_to_one",
        )
    )

    # --------------------------------------------------
    # Distance and Location Features
    # --------------------------------------------------

    final_df["seller_customer_distance_km"] = calculate_haversine_distance(
        final_df["seller_lat"],
        final_df["seller_lng"],
        final_df["customer_lat"],
        final_df["customer_lng"],
    )

    final_df["distance_bucket"] = pd.cut(
        final_df["seller_customer_distance_km"],
        bins=[0, 50, 200, 500, 1000, 2000, np.inf],
        labels=[
            "0-50 km",
            "50-200 km",
            "200-500 km",
            "500-1000 km",
            "1000-2000 km",
            "2000+ km",
        ],
        include_lowest=True,
    )

    final_df["seller_customer_same_state"] = np.where(
        final_df["seller_state"] == final_df["customer_state"],
        1,
        0,
    )

    final_df["seller_customer_same_city"] = np.where(
        final_df["seller_city"] == final_df["customer_city"],
        1,
        0,
    )

    # --------------------------------------------------
    # Final Cleanup
    # --------------------------------------------------

    final_df = final_df.replace([np.inf, -np.inf], np.nan)
    final_df = final_df.drop_duplicates()

    missing_columns = [
        column for column in FINAL_GOLD_COLUMNS
        if column not in final_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required gold-layer columns:\n"
            + "\n".join(missing_columns)
        )

    final_df = final_df[FINAL_GOLD_COLUMNS]

    return final_df