from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RISK_SCORE_PATH = PROJECT_ROOT / "data/predictions/delivery_risk_scores.csv"
FEATURE_DATA_PATH = PROJECT_ROOT / "data/processed/feature_dataset.csv"


@st.cache_data
def load_dashboard_data() -> pd.DataFrame:
    """Load risk scores and target values for dashboard review."""
    risk_scores = pd.read_csv(RISK_SCORE_PATH)
    features = pd.read_csv(FEATURE_DATA_PATH, usecols=["sla_breached"])
    return risk_scores.join(features)


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters."""
    st.sidebar.header("Filters")

    customer_states = sorted(data["customer_state"].dropna().unique())
    seller_states = sorted(data["seller_state"].dropna().unique())
    categories = sorted(data["product_category_name"].dropna().unique())
    buckets = ["Low", "Medium", "High", "Critical"]

    selected_customer_states = st.sidebar.multiselect(
        "Customer state",
        customer_states,
        default=customer_states,
    )
    selected_seller_states = st.sidebar.multiselect(
        "Seller state",
        seller_states,
        default=seller_states,
    )
    selected_categories = st.sidebar.multiselect(
        "Product category",
        categories,
        default=categories,
    )
    selected_buckets = st.sidebar.multiselect(
        "Risk bucket",
        buckets,
        default=buckets,
    )

    return data[
        data["customer_state"].isin(selected_customer_states)
        & data["seller_state"].isin(selected_seller_states)
        & data["product_category_name"].isin(selected_categories)
        & data["risk_bucket"].isin(selected_buckets)
    ]


def render_metrics(data: pd.DataFrame) -> None:
    """Render top-level dashboard metrics."""
    total_orders = len(data)
    breach_rate = data["sla_breached"].mean() if total_orders else 0
    high_or_critical = data["risk_bucket"].isin(["High", "Critical"]).sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total orders scored", f"{total_orders:,}")
    col2.metric("Actual SLA breach rate", f"{breach_rate:.2%}")
    col3.metric("High/Critical risk orders", f"{high_or_critical:,}")


def render_charts(data: pd.DataFrame) -> None:
    """Render dashboard charts."""
    bucket_order = ["Low", "Medium", "High", "Critical"]
    bucket_counts = (
        data["risk_bucket"]
        .value_counts()
        .reindex(bucket_order, fill_value=0)
        .rename_axis("risk_bucket")
        .reset_index(name="orders")
    )
    st.subheader("Risk bucket summary")
    st.bar_chart(bucket_counts.set_index("risk_bucket"))

    st.subheader("SLA breach probability distribution")
    st.bar_chart(data["sla_breach_probability"].round(2).value_counts().sort_index())

    st.subheader("Average risk by customer state")
    customer_state_risk = (
        data.groupby("customer_state")["sla_breach_probability"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )
    st.bar_chart(customer_state_risk)

    st.subheader("Average risk by seller state")
    seller_state_risk = (
        data.groupby("seller_state")["sla_breach_probability"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )
    st.bar_chart(seller_state_risk)

    st.subheader("Average risk by product category")
    category_risk = (
        data.groupby("product_category_name")["sla_breach_probability"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )
    st.bar_chart(category_risk)


def render_high_risk_table(data: pd.DataFrame) -> None:
    """Render high-risk orders."""
    st.subheader("High-risk order table")
    high_risk = data[data["risk_bucket"].isin(["High", "Critical"])].sort_values(
        "sla_breach_probability",
        ascending=False,
    )
    st.dataframe(
        high_risk[
            [
                "order_id",
                "sla_breach_probability",
                "risk_bucket",
                "customer_state",
                "seller_state",
                "product_category_name",
                "estimated_delivery_days",
                "top_risk_reason",
            ]
        ].head(200),
        use_container_width=True,
    )


def main() -> None:
    """Run the Streamlit dashboard."""
    st.set_page_config(page_title="DeliverIQ Risk Dashboard", layout="wide")
    st.title("DeliverIQ SLA Breach Risk Dashboard")

    if not RISK_SCORE_PATH.exists():
        st.error("Risk scores not found. Run `python -m src.models.predict` first.")
        return

    data = load_dashboard_data()
    filtered_data = apply_filters(data)

    render_metrics(filtered_data)
    render_charts(filtered_data)
    render_high_risk_table(filtered_data)


if __name__ == "__main__":
    main()
