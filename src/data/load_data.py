from pathlib import Path
from typing import Dict, Iterable, Optional

import pandas as pd
import yaml


DEFAULT_OLIST_TABLES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
}


def load_config(config_path: str = "config.yaml") -> dict:
    """Load project configuration from YAML."""
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_csv_table(file_path: str | Path) -> pd.DataFrame:
    """Load one CSV file as a pandas DataFrame."""
    return pd.read_csv(file_path)


def load_olist_tables(
    raw_dir: str | Path = "data/raw",
    table_files: Optional[dict[str, str]] = None,
    required_tables: Optional[Iterable[str]] = None,
) -> Dict[str, pd.DataFrame]:
    """Load the Olist tables needed to build the order-level base dataset."""
    raw_path = Path(raw_dir)
    files = table_files or DEFAULT_OLIST_TABLES

    if required_tables is None:
        required_tables = DEFAULT_OLIST_TABLES.keys()

    selected_files = {table: files[table] for table in required_tables}
    dataframes = {}
    missing_files = []

    for table_name, file_name in selected_files.items():
        file_path = raw_path / file_name

        if not file_path.exists():
            missing_files.append(str(file_path))
            continue

        dataframes[table_name] = load_csv_table(file_path)

    if missing_files:
        raise FileNotFoundError(
            "Missing required input files:\n" + "\n".join(missing_files)
        )

    return dataframes


def load_raw_data(config: dict) -> Dict[str, pd.DataFrame]:
    """Read all raw CSV files defined in config.yaml."""
    return load_olist_tables(
        raw_dir=config["paths"]["raw_dir"],
        table_files=config["files"],
        required_tables=config["files"].keys(),
    )


def save_dataframes(
    dataframes: Dict[str, pd.DataFrame],
    output_dir: str,
    file_map: Optional[dict] = None,
) -> None:
    """Save multiple dataframes as CSV files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for table_name, df in dataframes.items():
        if file_map and table_name in file_map:
            file_name = file_map[table_name]
        else:
            file_name = f"{table_name}.csv"

        df.to_csv(output_path / file_name, index=False)
