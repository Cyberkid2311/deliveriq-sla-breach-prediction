from pathlib import Path

import pandas as pd


DEFAULT_INPUT_PATH = Path("data/processed/modeling_dataset_v1.csv")
DEFAULT_OUTPUT_PATH = Path("data/processed/feature_dataset.csv")

DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_estimated_delivery_date",
]

SOURCE_TO_FEATURE_COLUMNS = {
    "primary_seller_city": "seller_city",
    "primary_seller_state": "seller_state",
    "primary_product_category_name": "product_category_name",
    "avg_product_weight_g": "product_weight_g",
    "total_product_weight_g": "total_product_weight_g",
    "avg_product_length_cm": "product_length_cm",
    "avg_product_height_cm": "product_height_cm",
    "avg_product_width_cm": "product_width_cm",
    "avg_product_volume_cm3": "product_volume_cm3",
    "total_product_volume_cm3": "total_product_volume_cm3",
    "total_freight_value": "freight_value",
    "avg_freight_value": "avg_freight_value",
    "total_price": "price",
    "avg_price": "avg_price",
}

TEXT_FEATURES = [
    "customer_state",
    "customer_city",
    "seller_state",
    "seller_city",
    "product_category_name",
]

NUMERIC_FEATURES = [
    "estimated_delivery_days",
    "product_weight_g",
    "product_weight_kg",
    "total_product_weight_g",
    "total_product_weight_kg",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "product_volume_cm3",
    "total_product_volume_cm3",
    "freight_value",
    "avg_freight_value",
    "price",
    "avg_price",
    "item_count",
    "product_count",
    "seller_count",
    "product_category_count",
    "price_per_item",
    "freight_per_item",
    "seller_customer_same_zip_prefix",
]

FINAL_FEATURE_COLUMNS = [
    "purchase_day_of_week",
    "purchase_hour",
    "is_weekend_order",
    "estimated_delivery_days",
    "customer_state",
    "customer_city",
    "seller_state",
    "seller_city",
    "seller_customer_same_state",
    "seller_customer_same_city",
    "seller_customer_same_zip_prefix",
    "product_category_name",
    "product_weight_g",
    "product_weight_kg",
    "total_product_weight_g",
    "total_product_weight_kg",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "product_volume_cm3",
    "total_product_volume_cm3",
    "product_weight_bucket",
    "freight_value",
    "avg_freight_value",
    "freight_value_bucket",
    "price",
    "avg_price",
    "item_count",
    "product_count",
    "seller_count",
    "product_category_count",
    "price_per_item",
    "freight_per_item",
    "sla_breached",
]

LEAKAGE_COLUMNS = [
    "order_id",
    "customer_id",
    "customer_unique_id",
    "primary_product_id",
    "primary_seller_id",
    "order_status",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "actual_delivery_days",
    "delivery_delay_days",
]


def load_modeling_dataset(input_path: str | Path = DEFAULT_INPUT_PATH) -> pd.DataFrame:
    """Load the Day 2 modeling dataset."""
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Modeling dataset not found: {input_path}")

    return pd.read_csv(input_path)


def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date columns needed for feature creation."""
    df = df.copy()

    for column in DATE_COLUMNS:
        if column not in df.columns:
            raise ValueError(f"Missing required date column: {column}")
        df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def standardize_order_level_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map current order-level aggregate fields to the feature names in the task sheet.

    For multi-item orders, commercial values use order totals while product physical
    attributes use average item attributes created in the base order dataset.
    """
    df = df.copy()
    missing_sources = [
        source for source in SOURCE_TO_FEATURE_COLUMNS if source not in df.columns
    ]

    if missing_sources:
        raise ValueError(
            "Missing source columns required for feature mapping:\n"
            + "\n".join(missing_sources)
        )

    return df.rename(columns=SOURCE_TO_FEATURE_COLUMNS)


def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create model-safe time-based features."""
    df = df.copy()
    df["purchase_day_of_week"] = df["order_purchase_timestamp"].dt.dayofweek
    df["purchase_hour"] = df["order_purchase_timestamp"].dt.hour
    df["is_weekend_order"] = df["purchase_day_of_week"].isin([5, 6]).astype("int64")
    df["estimated_delivery_days"] = (
        df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / (60 * 60 * 24)
    return df


def handle_missing_location_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing location fields with an explicit unknown category."""
    df = df.copy()

    for column in ["customer_city", "seller_city"]:
        df[column] = df[column].astype("string").str.strip().str.lower().fillna("unknown")

    for column in ["customer_state", "seller_state"]:
        df[column] = df[column].astype("string").str.strip().str.upper().fillna("UNKNOWN")

    return df


def handle_missing_product_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing product category and numeric product attributes."""
    df = df.copy()
    df["product_category_name"] = (
        df["product_category_name"]
        .astype("string")
        .str.strip()
        .str.lower()
        .fillna("unknown")
    )

    product_numeric_columns = [
        "product_weight_g",
        "total_product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
        "total_product_volume_cm3",
    ]

    for column in product_numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        df[column] = df[column].fillna(df[column].median())

    return df


def handle_missing_commercial_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing order-level price, freight, and item-count fields."""
    df = df.copy()

    for column in ["freight_value", "price", "item_count", "avg_price", "avg_freight_value"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
        else:
            df[column] = 0.0

    valid_item_count = df["item_count"] > 0
    df.loc[valid_item_count, "avg_price"] = df.loc[valid_item_count, "avg_price"].fillna(
        df.loc[valid_item_count, "price"] / df.loc[valid_item_count, "item_count"]
    )
    df.loc[valid_item_count, "avg_freight_value"] = df.loc[valid_item_count, "avg_freight_value"].fillna(
        df.loc[valid_item_count, "freight_value"] / df.loc[valid_item_count, "item_count"]
    )

    df["avg_price"] = df["avg_price"].fillna(0)
    df["avg_freight_value"] = df["avg_freight_value"].fillna(0)
    df["item_count"] = df["item_count"].fillna(0).astype("int64")

    return df


def create_location_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create same-city and same-state seller/customer flags."""
    df = df.copy()
    df["seller_customer_same_state"] = (
        df["seller_state"] == df["customer_state"]
    ).astype("int64")
    df["seller_customer_same_city"] = (
        df["seller_city"] == df["customer_city"]
    ).astype("int64")
    return df


def create_product_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create product volume, weight in kg, and weight bucket features."""
    df = df.copy()
    df["product_volume_cm3"] = (
        df["product_length_cm"] * df["product_height_cm"] * df["product_width_cm"]
    )
    df["product_weight_kg"] = df["product_weight_g"] / 1000
    df["total_product_weight_kg"] = df["total_product_weight_g"] / 1000
    df["product_weight_bucket"] = pd.cut(
        df["product_weight_g"],
        bins=[0, 500, 1000, 5000, 10000, float("inf")],
        labels=[
            "0-500g",
            "500g-1kg",
            "1-5kg",
            "5-10kg",
            "10kg+",
        ],
        include_lowest=True,
    ).astype("string")
    return df


def create_commercial_intensity_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create per-item commercial intensity features."""
    df = df.copy()
    df["price_per_item"] = df["price"] / df["item_count"]
    df["freight_per_item"] = df["freight_value"] / df["item_count"]

    df.loc[df["item_count"] == 0, "price_per_item"] = 0
    df.loc[df["item_count"] == 0, "freight_per_item"] = 0

    return df


def create_zip_prefix_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create a simple proximity signal from seller and customer zip prefixes."""
    df = df.copy()
    df["seller_customer_same_zip_prefix"] = (
        df["primary_seller_zip_code_prefix"].astype("string").str.strip()
        == df["customer_zip_code_prefix"].astype("string").str.strip()
    ).astype("int64")
    return df


def create_freight_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create an order-level freight value bucket."""
    df = df.copy()
    df["freight_value_bucket"] = pd.cut(
        df["freight_value"],
        bins=[-0.01, 15, 30, 60, 100, float("inf")],
        labels=[
            "0-15",
            "15-30",
            "30-60",
            "60-100",
            "100+",
        ],
        include_lowest=True,
    ).astype("string")
    return df


def remove_leakage_and_select_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return only approved features and the target column."""
    missing_final_columns = [
        column for column in FINAL_FEATURE_COLUMNS if column not in df.columns
    ]

    if missing_final_columns:
        raise ValueError(
            "Missing final feature dataset columns:\n" + "\n".join(missing_final_columns)
        )

    feature_dataset = df[FINAL_FEATURE_COLUMNS].copy()

    leaked_columns = [
        column for column in LEAKAGE_COLUMNS if column in feature_dataset.columns
    ]
    if leaked_columns:
        raise ValueError(
            "Leakage columns found in final feature dataset:\n"
            + "\n".join(leaked_columns)
        )

    return feature_dataset


def validate_feature_dataset(df: pd.DataFrame) -> None:
    """Validate the final ML-ready feature dataset."""
    if "sla_breached" not in df.columns:
        raise ValueError("Missing target column: sla_breached")

    invalid_target_values = set(df["sla_breached"].dropna().unique()) - {0, 1}
    if invalid_target_values:
        raise ValueError(f"Invalid target values: {invalid_target_values}")

    if df["sla_breached"].isna().any():
        raise ValueError("Target column contains missing values.")

    if df.drop(columns=["sla_breached"]).isna().any().any():
        missing_counts = df.drop(columns=["sla_breached"]).isna().sum()
        missing_counts = missing_counts[missing_counts > 0]
        raise ValueError(
            "Feature dataset contains missing feature values:\n"
            + missing_counts.to_string()
        )


def build_feature_dataset(modeling_dataset: pd.DataFrame) -> pd.DataFrame:
    """Build a clean ML-ready dataset with approved features and target only."""
    features = convert_date_columns(modeling_dataset)
    features = standardize_order_level_column_names(features)
    features = create_time_features(features)
    features = handle_missing_location_fields(features)
    features = handle_missing_product_fields(features)
    features = handle_missing_commercial_fields(features)
    features = create_location_features(features)
    features = create_zip_prefix_features(features)
    features = create_commercial_intensity_features(features)
    features = create_product_features(features)
    features = create_freight_features(features)
    features = remove_leakage_and_select_features(features)

    validate_feature_dataset(features)

    return features


def save_feature_dataset(
    feature_dataset: pd.DataFrame,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> None:
    """Save the final feature dataset."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    feature_dataset.to_csv(output_path, index=False)


def main(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> pd.DataFrame:
    """Run the full feature build pipeline."""
    modeling_dataset = load_modeling_dataset(input_path)
    feature_dataset = build_feature_dataset(modeling_dataset)
    save_feature_dataset(feature_dataset, output_path)
    return feature_dataset


if __name__ == "__main__":
    dataset = main()
    print(f"Saved {DEFAULT_OUTPUT_PATH} with shape {dataset.shape}")
