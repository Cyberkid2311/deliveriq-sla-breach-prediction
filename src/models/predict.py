from __future__ import annotations

from pathlib import Path
import pickle
from typing import Any

import pandas as pd

try:
    from src.models.model_selection import assign_risk_bucket
    from src.models.train_baseline import PROJECT_ROOT, resolve_project_path
except ModuleNotFoundError:
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.models.model_selection import assign_risk_bucket
    from src.models.train_baseline import PROJECT_ROOT, resolve_project_path


DEFAULT_MODEL_PATH = PROJECT_ROOT / "models/final_model.pkl"
DEFAULT_FEATURE_PATH = PROJECT_ROOT / "data/processed/feature_dataset.csv"
DEFAULT_MODELING_PATH = PROJECT_ROOT / "data/processed/modeling_dataset_v1.csv"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "data/predictions/delivery_risk_scores.csv"


def load_model(model_path: str | Path = DEFAULT_MODEL_PATH) -> Any:
    """Load the final SLA breach model artifact."""
    model_path = resolve_project_path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {model_path}")

    with model_path.open("rb") as file:
        return pickle.load(file)


def get_expected_feature_columns(model: Any) -> list[str]:
    """Read the pipeline preprocessor input columns from a fitted model."""
    preprocessor = model.named_steps.get("preprocessor")
    if preprocessor is None:
        raise ValueError("Final model must be a pipeline with a preprocessor step.")

    columns: list[str] = []
    for _, _, transformer_columns in preprocessor.transformers_:
        if transformer_columns == "drop":
            continue
        columns.extend(list(transformer_columns))
    return columns


def create_top_risk_reason(row: pd.Series) -> str:
    """Create a simple business-friendly reason from model-safe feature values."""
    reasons = []

    if row.get("seller_customer_same_state", 1) == 0:
        reasons.append("cross-state route")
    if row.get("freight_value", 0) >= 60:
        reasons.append("high freight value")
    if row.get("estimated_delivery_days", 0) >= 15:
        reasons.append("long delivery estimate")
    if row.get("product_weight_kg", 0) >= 5:
        reasons.append("heavy shipment")
    if row.get("is_weekend_order", 0) == 1:
        reasons.append("weekend order")

    return ", ".join(reasons[:3]) if reasons else "standard risk pattern"


def generate_risk_scores(
    model: Any,
    feature_dataset: pd.DataFrame,
    modeling_dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Generate order-level SLA breach probabilities and risk buckets."""
    feature_columns = get_expected_feature_columns(model)
    missing_columns = sorted(set(feature_columns) - set(feature_dataset.columns))
    if missing_columns:
        raise ValueError("Missing model input columns:\n" + "\n".join(missing_columns))

    probabilities = model.predict_proba(feature_dataset[feature_columns])[:, 1]

    output = pd.DataFrame(
        {
            "order_id": modeling_dataset["order_id"].values,
            "sla_breach_probability": probabilities,
            "risk_bucket": [assign_risk_bucket(value) for value in probabilities],
            "customer_state": feature_dataset["customer_state"].values,
            "seller_state": feature_dataset["seller_state"].values,
            "product_category_name": feature_dataset["product_category_name"].values,
            "estimated_delivery_days": feature_dataset[
                "estimated_delivery_days"
            ].values,
        }
    )
    output["top_risk_reason"] = feature_dataset.apply(create_top_risk_reason, axis=1)
    return output


def save_risk_scores(
    risk_scores: pd.DataFrame,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> None:
    """Save the prediction output CSV."""
    output_path = resolve_project_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    risk_scores.to_csv(output_path, index=False)


def run_prediction(
    model_path: str | Path = DEFAULT_MODEL_PATH,
    feature_path: str | Path = DEFAULT_FEATURE_PATH,
    modeling_path: str | Path = DEFAULT_MODELING_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> pd.DataFrame:
    """Run the full Day 6 risk scoring workflow."""
    model = load_model(model_path)
    feature_dataset = pd.read_csv(resolve_project_path(feature_path))
    modeling_dataset = pd.read_csv(resolve_project_path(modeling_path))

    if len(feature_dataset) != len(modeling_dataset):
        raise ValueError("Feature and modeling datasets must have the same row count.")

    risk_scores = generate_risk_scores(model, feature_dataset, modeling_dataset)
    save_risk_scores(risk_scores, output_path)
    return risk_scores


def main() -> None:
    """Generate delivery risk scores for all orders."""
    risk_scores = run_prediction()
    print(f"Saved {DEFAULT_OUTPUT_PATH} with shape {risk_scores.shape}")


if __name__ == "__main__":
    main()
