import logging
from pathlib import Path

from src.data.load_data import load_config, load_raw_data, save_dataframes
from src.data.process_data import build_final_dataset, process_to_silver


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def run_pipeline(config_path: str = "config.yaml") -> None:
    """Run the complete raw -> silver -> gold data pipeline."""
    logging.info("Pipeline started")

    config = load_config(config_path)

    raw_dir = config["paths"]["raw_dir"]
    silver_dir = config["paths"]["silver_dir"]
    gold_dir = config["paths"]["gold_dir"]
    final_dataset_name = config["outputs"]["final_dataset"]

    logging.info("Reading raw data from: %s", raw_dir)
    raw_dataframes = load_raw_data(config)

    for table_name, df in raw_dataframes.items():
        logging.info(f"Loaded raw table: {table_name} | shape={df.shape}")

    logging.info("Processing raw data into silver layer")
    silver_dataframes = process_to_silver(raw_dataframes)

    logging.info(f"Saving cleaned silver data to: {silver_dir}", )
    save_dataframes(
        dataframes=silver_dataframes,
        output_dir=silver_dir,
        file_map=config["files"],
    )

    for table_name, df in silver_dataframes.items():
        logging.info(f"Saved silver table: {table_name} | shape={df.shape}")

    logging.info("Building final gold consumption dataset")
    final_df = build_final_dataset(silver_dataframes)

    gold_path = Path(gold_dir)
    gold_path.mkdir(parents=True, exist_ok=True)

    final_output_path = gold_path / final_dataset_name
    final_df.to_csv(final_output_path, index=False)

    logging.info(f"Saved final dataset: {final_output_path}")
    logging.info(f"Final dataset shape: {final_df.shape}")
    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()