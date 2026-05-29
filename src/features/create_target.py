from pathlib import Path

import pandas as pd


DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

DEFAULT_INPUT_PATH = Path("data/processed/base_order_dataset.csv")
DEFAULT_OUTPUT_PATH = Path("data/processed/modeling_dataset_v1.csv")

STRING_COLUMNS = [
    "order_id",
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",
    "primary_product_id",
    "primary_product_category_name",
    "primary_seller_id",
    "primary_seller_zip_code_prefix",
    "primary_seller_city",
    "primary_seller_state",
]


def load_base_order_dataset(input_path: str | Path = DEFAULT_INPUT_PATH) -> pd.DataFrame:
    """Load the one-row-per-order base dataset."""
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Base order dataset not found: {input_path}")

    return pd.read_csv(input_path, dtype={column: "string" for column in STRING_COLUMNS})


def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert order date columns to pandas datetime dtype."""
    df = df.copy()

    for column in DATE_COLUMNS:
        if column not in df.columns:
            raise ValueError(f"Missing required date column: {column}")

        df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def filter_usable_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep MVP records where the SLA breach label can be created reliably.

    Canceled and unavailable orders are excluded from this first modeling dataset.
    """
    required_columns = [
        "order_status",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError("Missing required filter columns:\n" + "\n".join(missing_columns))

    usable_orders = df[
        (df["order_status"].str.lower() == "delivered")
        & df["order_delivered_customer_date"].notna()
        & df["order_estimated_delivery_date"].notna()
    ].copy()

    return usable_orders


def add_sla_target(df: pd.DataFrame) -> pd.DataFrame:
    """Create the SLA breach target column."""
    df = df.copy()
    df["sla_breached"] = (
        df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    ).astype("int64")
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create basic time-based columns for modeling and EDA.

    actual_delivery_days and delivery_delay_days depend on the actual delivery date,
    so keep them for EDA only and exclude them from model input features.
    """
    df = df.copy()

    df["estimated_delivery_days"] = (
        df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / (60 * 60 * 24)

    df["actual_delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / (60 * 60 * 24)

    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.total_seconds() / (60 * 60 * 24)

    df["purchase_day_of_week"] = df["order_purchase_timestamp"].dt.dayofweek
    df["purchase_hour"] = df["order_purchase_timestamp"].dt.hour
    df["is_weekend_order"] = df["purchase_day_of_week"].isin([5, 6]).astype("int64")

    return df


def validate_modeling_dataset(df: pd.DataFrame) -> None:
    """Validate the expected MVP modeling dataset grain and target fields."""
    if "order_id" not in df.columns:
        raise ValueError("Missing required identifier column: order_id")

    if df["order_id"].duplicated().any():
        duplicate_count = int(df["order_id"].duplicated().sum())
        raise ValueError(
            f"Modeling dataset is not order-level: {duplicate_count} duplicate order_id rows."
        )

    if df["sla_breached"].isna().any():
        raise ValueError("Target column sla_breached contains missing values.")

    invalid_target_values = set(df["sla_breached"].unique()) - {0, 1}
    if invalid_target_values:
        raise ValueError(f"Invalid sla_breached values: {invalid_target_values}")


def create_modeling_dataset(base_orders: pd.DataFrame) -> pd.DataFrame:
    """Create the first clean ML-ready dataset with the SLA breach target."""
    modeling_dataset = convert_date_columns(base_orders)
    modeling_dataset = filter_usable_orders(modeling_dataset)
    modeling_dataset = add_sla_target(modeling_dataset)
    modeling_dataset = add_time_features(modeling_dataset)
    modeling_dataset = modeling_dataset.sort_values("order_id").reset_index(drop=True)

    validate_modeling_dataset(modeling_dataset)

    return modeling_dataset


def save_modeling_dataset(
    modeling_dataset: pd.DataFrame,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> None:
    """Save the first modeling dataset."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    modeling_dataset.to_csv(output_path, index=False)


def main(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> pd.DataFrame:
    """Run the full target creation pipeline."""
    base_orders = load_base_order_dataset(input_path)
    modeling_dataset = create_modeling_dataset(base_orders)
    save_modeling_dataset(modeling_dataset, output_path)
    return modeling_dataset


if __name__ == "__main__":
    dataset = main()
    print(f"Saved {DEFAULT_OUTPUT_PATH} with shape {dataset.shape}")
