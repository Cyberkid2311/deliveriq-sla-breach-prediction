from __future__ import annotations

from typing import Any

import pandas as pd


RISK_BUCKETS = [
    (0.00, 0.30, "Low", "No action"),
    (0.30, 0.60, "Medium", "Monitor"),
    (0.60, 0.80, "High", "Prioritize"),
    (0.80, 1.00, "Critical", "Immediate intervention"),
]


def assign_risk_bucket(probability: float) -> str:
    """Assign an operational risk bucket from an SLA breach probability."""
    if probability <= 0.30:
        return "Low"
    if probability <= 0.60:
        return "Medium"
    if probability <= 0.80:
        return "High"
    return "Critical"


def risk_bucket_action(risk_bucket: str) -> str:
    """Return the recommended action for a risk bucket."""
    actions = {
        "Low": "No action",
        "Medium": "Monitor",
        "High": "Prioritize",
        "Critical": "Immediate intervention",
    }
    return actions.get(risk_bucket, "Review")


def select_final_model(
    model_metrics: pd.DataFrame,
    model_objects: dict[str, Any],
) -> tuple[str, Any, pd.Series]:
    """Select the final model by the project priority order."""
    ranked = model_metrics.sort_values(
        by=[
            "recall_class_1",
            "precision_class_1",
            "f1_class_1",
            "pr_auc",
            "roc_auc",
        ],
        ascending=False,
    )
    final_row = ranked.iloc[0]
    final_model_name = final_row["model"]
    return final_model_name, model_objects[final_model_name], final_row


def format_risk_bucket_logic() -> str:
    """Render risk bucket logic as a Markdown table."""
    lines = [
        "| Probability Range | Risk Bucket | Action |",
        "| ---: | --- | --- |",
    ]
    for low, high, bucket, action in RISK_BUCKETS:
        if bucket == "Low":
            probability_range = f"{low:.2f}-{high:.2f}"
        else:
            probability_range = f">{low:.2f}-{high:.2f}"
        lines.append(f"| {probability_range} | {bucket} | {action} |")
    return "\n".join(lines)
