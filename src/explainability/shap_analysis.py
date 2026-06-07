from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

try:
    from src.models.predict import (
        DEFAULT_FEATURE_PATH,
        DEFAULT_MODEL_PATH,
        load_model,
    )
    from src.models.train_baseline import PROJECT_ROOT, resolve_project_path
except ModuleNotFoundError:
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.models.predict import (
        DEFAULT_FEATURE_PATH,
        DEFAULT_MODEL_PATH,
        load_model,
    )
    from src.models.train_baseline import PROJECT_ROOT, resolve_project_path


REPORT_PATH = PROJECT_ROOT / "reports/model_explainability_report.md"
IMPORTANCE_PATH = PROJECT_ROOT / "reports/model_feature_importance.csv"


BUSINESS_FEATURE_EXPLANATIONS = {
    "estimated_delivery_days": "Long promised delivery window",
    "freight_value": "Costlier or more complex shipment",
    "seller_customer_same_state": "Cross-state delivery signal",
    "seller_customer_same_city": "Cross-city delivery signal",
    "customer_state": "Destination region pattern",
    "seller_state": "Seller origin region pattern",
    "product_category_name": "Product category delay pattern",
    "is_weekend_order": "Weekend operational delay effect",
    "product_weight": "Heavy shipment complexity",
}


def get_transformed_feature_names(model: Any) -> list[str]:
    """Return transformed feature names from a fitted pipeline."""
    preprocessor = model.named_steps.get("preprocessor")
    if preprocessor is None:
        raise ValueError("Model must contain a preprocessor step.")

    try:
        return list(preprocessor.get_feature_names_out())
    except AttributeError:
        return [f"feature_{index}" for index in range(preprocessor.transform(None).shape[1])]


def extract_model_importance(model: Any) -> pd.DataFrame:
    """Extract coefficient or feature importance values from the final estimator."""
    estimator = model.named_steps.get("model")
    feature_names = get_transformed_feature_names(model)

    if hasattr(estimator, "coef_"):
        values = estimator.coef_[0]
        importance = abs(values)
    elif hasattr(estimator, "feature_importances_"):
        importance = estimator.feature_importances_
        values = importance
    else:
        raise ValueError("Final estimator does not expose coefficients or importances.")

    return pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importance,
            "signed_value": values,
        }
    ).sort_values("importance", ascending=False)


def map_business_explanation(feature_name: str) -> str:
    """Map technical feature names to simple business explanations."""
    for signal, explanation in BUSINESS_FEATURE_EXPLANATIONS.items():
        if signal in feature_name:
            return explanation
    return "Historical pattern learned from approved pre-delivery features"


def attempt_shap_summary(model: Any, X_sample: pd.DataFrame) -> str:
    """Attempt SHAP analysis if the optional dependency is installed."""
    try:
        import shap  # type: ignore
    except ModuleNotFoundError:
        return "SHAP was not run because the optional `shap` package is not installed."

    try:
        explainer = shap.Explainer(model.predict_proba, X_sample)
        shap_values = explainer(X_sample)
        return f"SHAP ran successfully on {len(shap_values)} sampled rows."
    except Exception as error:  # pragma: no cover - defensive optional path
        return f"SHAP was attempted but did not complete: {error}"


def generate_explainability_report(
    importance: pd.DataFrame,
    shap_status: str,
) -> str:
    """Create the Day 6 explainability report."""
    top_features = importance.head(10).copy()
    top_features["business_explanation"] = top_features["feature"].map(
        map_business_explanation
    )

    lines = [
        "# Model Explainability Report",
        "",
        "## Summary",
        "",
        "The final model is explained using model-native feature importance. SHAP analysis is attempted when the optional `shap` package is available.",
        "",
        "## Top 10 Model Drivers",
        "",
        "| Rank | Feature | Importance | Business Explanation |",
        "| ---: | --- | ---: | --- |",
    ]

    for rank, row in enumerate(top_features.itertuples(index=False), start=1):
        lines.append(
            f"| {rank} | `{row.feature}` | {row.importance:.6f} | {row.business_explanation} |"
        )

    lines.extend(
        [
            "",
            "## SHAP Status",
            "",
            shap_status,
            "",
            "## Example High-Risk Explanation",
            "",
            "A high-risk order may be flagged because it combines signals such as a cross-state route, high freight value, long estimated delivery window, heavier shipment, or a historically riskier destination/product pattern.",
            "",
        ]
    )
    return "\n".join(lines)


def save_outputs(
    importance: pd.DataFrame,
    report: str,
    importance_path: str | Path = IMPORTANCE_PATH,
    report_path: str | Path = REPORT_PATH,
) -> None:
    """Save feature importance and report outputs."""
    importance_path = resolve_project_path(importance_path)
    report_path = resolve_project_path(report_path)
    importance_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    importance.to_csv(importance_path, index=False)
    report_path.write_text(report, encoding="utf-8")


def run_explainability(
    model_path: str | Path = DEFAULT_MODEL_PATH,
    feature_path: str | Path = DEFAULT_FEATURE_PATH,
) -> pd.DataFrame:
    """Run final-model explainability and save outputs."""
    model = load_model(model_path)
    feature_dataset = pd.read_csv(resolve_project_path(feature_path))

    preprocessor = model.named_steps["preprocessor"]
    feature_columns: list[str] = []
    for _, _, transformer_columns in preprocessor.transformers_:
        if transformer_columns != "drop":
            feature_columns.extend(list(transformer_columns))

    importance = extract_model_importance(model)
    shap_status = attempt_shap_summary(model, feature_dataset[feature_columns].head(100))
    report = generate_explainability_report(importance, shap_status)
    save_outputs(importance, report)
    return importance


def main() -> None:
    """Run Day 6 explainability."""
    importance = run_explainability()
    print(importance.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
