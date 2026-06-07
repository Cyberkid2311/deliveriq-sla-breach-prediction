from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RISK_SCORE_PATH = PROJECT_ROOT / "data/predictions/delivery_risk_scores.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports/dashboard_screenshots"


def save_bar_chart(
    series: pd.Series,
    title: str,
    ylabel: str,
    output_path: Path,
    rotation: int = 0,
) -> None:
    """Save a compact dashboard-style bar chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    series.plot(kind="bar", ax=ax, color="#2563eb")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=rotation)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def create_dashboard_screenshots(
    risk_score_path: str | Path = RISK_SCORE_PATH,
    output_dir: str | Path = OUTPUT_DIR,
) -> list[Path]:
    """Create dashboard chart screenshots from the risk score output."""
    risk_score_path = Path(risk_score_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    risk_scores = pd.read_csv(risk_score_path)
    bucket_order = ["Low", "Medium", "High", "Critical"]

    outputs = []

    bucket_counts = risk_scores["risk_bucket"].value_counts().reindex(
        bucket_order,
        fill_value=0,
    )
    output_path = output_dir / "risk_bucket_distribution.png"
    save_bar_chart(
        bucket_counts,
        "Risk Bucket Distribution",
        "Orders",
        output_path,
    )
    outputs.append(output_path)

    customer_state_risk = (
        risk_scores.groupby("customer_state")["sla_breach_probability"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    output_path = output_dir / "risk_by_customer_state.png"
    save_bar_chart(
        customer_state_risk,
        "Average Risk By Customer State",
        "Average SLA Breach Probability",
        output_path,
    )
    outputs.append(output_path)

    category_risk = (
        risk_scores.groupby("product_category_name")["sla_breach_probability"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    output_path = output_dir / "risk_by_product_category.png"
    save_bar_chart(
        category_risk,
        "Average Risk By Product Category",
        "Average SLA Breach Probability",
        output_path,
        rotation=45,
    )
    outputs.append(output_path)

    return outputs


def main() -> None:
    """Create dashboard screenshots and print their paths."""
    outputs = create_dashboard_screenshots()
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
