from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import yaml


def load_config(config_path: str = "config.yaml") -> dict:
    """Load project configuration from YAML."""
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_raw_data(config: dict) -> Dict[str, pd.DataFrame]:
    """Read all raw CSV files defined in config.yaml."""
    raw_dir = Path(config["paths"]["raw_dir"])
    files = config["files"]

    dataframes = {}
    missing_files = []

    for table_name, file_name in files.items():
        file_path = raw_dir / file_name

        if not file_path.exists():
            missing_files.append(str(file_path))
            continue

        dataframes[table_name] = pd.read_csv(file_path)

    if missing_files:
        raise FileNotFoundError(
            "Missing required input files:\n" + "\n".join(missing_files)
        )

    return dataframes


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
