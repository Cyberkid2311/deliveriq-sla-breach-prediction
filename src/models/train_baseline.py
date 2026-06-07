from __future__ import annotations

from pathlib import Path
import pickle
from typing import Any

import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

try:
    from src.models.evaluate_model import evaluate_classifier, metrics_to_frame
except ModuleNotFoundError:
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.models.evaluate_model import evaluate_classifier, metrics_to_frame


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data/processed/feature_dataset.csv"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_PATH = PROJECT_ROOT / "reports/baseline_model_report.md"
TARGET_COLUMN = "sla_breached"
TEST_SIZE = 0.2
RANDOM_STATE = 42

APPROVED_MODEL_FEATURES = [
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
    "product_count",
    "seller_count",
    "product_category_count",
    "freight_value",
    "avg_freight_value",
    "freight_value_bucket",
    "price",
    "avg_price",
    "item_count",
    "price_per_item",
    "freight_per_item",
    "seller_customer_same_zip_prefix",
]

NUMERICAL_FEATURES = [
    "purchase_hour",
    "is_weekend_order",
    "estimated_delivery_days",
    "seller_customer_same_state",
    "seller_customer_same_city",
    "product_weight_g",
    "product_weight_kg",
    "total_product_weight_g",
    "total_product_weight_kg",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "product_volume_cm3",
    "total_product_volume_cm3",
    "product_count",
    "seller_count",
    "product_category_count",
    "freight_value",
    "avg_freight_value",
    "price",
    "avg_price",
    "item_count",
    "price_per_item",
    "freight_per_item",
    "seller_customer_same_zip_prefix",
]

CATEGORICAL_FEATURES = [
    "purchase_day_of_week",
    "customer_state",
    "customer_city",
    "seller_state",
    "seller_city",
    "product_category_name",
    "product_weight_bucket",
    "freight_value_bucket",
]

ID_COLUMNS = [
    "order_id",
    "customer_id",
    "customer_unique_id",
    "primary_product_id",
    "primary_seller_id",
]

LEAKAGE_COLUMNS = [
    "order_status",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "actual_delivery_days",
    "delivery_delay_days",
    "actual_delivery_time",
    "order_estimated_delivery_date",
    "review_id",
    "review_score",
    "review_comment_title",
    "review_comment_message",
    "review_creation_date",
    "review_answer_timestamp",
    "delay_reason",
    TARGET_COLUMN,
]

MODEL_DISPLAY_NAMES = {
    "logistic_regression": "Logistic Regression",
    "decision_tree": "Decision Tree",
    "random_forest": "Random Forest",
}

MODEL_ARTIFACT_NAMES = {
    "logistic_regression": "baseline_logistic_regression.pkl",
    "decision_tree": "baseline_decision_tree.pkl",
    "random_forest": "baseline_random_forest.pkl",
}


def resolve_project_path(path: str | Path) -> Path:
    """Resolve relative paths from the project root, not the current directory."""
    path = Path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def display_project_path(path: str | Path) -> str:
    """Format paths relative to the project root when possible."""
    path = resolve_project_path(path)
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def load_feature_dataset(input_path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load the approved order-level feature dataset."""
    input_path = resolve_project_path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Feature dataset not found: {input_path}")

    return pd.read_csv(input_path)


def separate_features_and_target(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Create X/y using approved model features and excluding IDs/leakage fields."""
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    blocked_columns = set(ID_COLUMNS + LEAKAGE_COLUMNS)
    model_features = [
        column
        for column in APPROVED_MODEL_FEATURES
        if column in df.columns and column not in blocked_columns
    ]
    missing_features = sorted(set(APPROVED_MODEL_FEATURES) - set(model_features))

    if missing_features:
        raise ValueError(
            "Missing approved model features:\n" + "\n".join(missing_features)
        )

    X = df[model_features].copy()
    y = df[TARGET_COLUMN].astype("int64")

    invalid_target_values = set(y.dropna().unique()) - {0, 1}
    if invalid_target_values:
        raise ValueError(f"Invalid target values: {invalid_target_values}")

    return X, y


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Create a stratified train/test split to preserve SLA breach ratio."""
    return train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Build preprocessing for numeric and categorical features."""
    numeric_features = [column for column in NUMERICAL_FEATURES if column in X.columns]
    categorical_features = [
        column for column in CATEGORICAL_FEATURES if column in X.columns
    ]
    assigned_features = set(numeric_features + categorical_features)
    unassigned_features = sorted(set(X.columns) - assigned_features)

    if unassigned_features:
        raise ValueError(
            "Features missing preprocessing assignment:\n"
            + "\n".join(unassigned_features)
        )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )


def build_model_candidates() -> dict[str, Any]:
    """Define baseline model candidates."""
    return {
        "logistic_regression": LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=RANDOM_STATE,
            solver="liblinear",
        ),
        "decision_tree": DecisionTreeClassifier(
            class_weight="balanced",
            max_depth=12,
            min_samples_leaf=100,
            random_state=RANDOM_STATE,
        ),
        "random_forest": RandomForestClassifier(
            class_weight="balanced",
            max_depth=18,
            min_samples_leaf=50,
            n_estimators=100,
            n_jobs=-1,
            random_state=RANDOM_STATE,
        ),
    }


def train_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor: ColumnTransformer,
) -> dict[str, Pipeline]:
    """Train each baseline model as a full preprocessing + estimator pipeline."""
    trained_models = {}

    for model_name, estimator in build_model_candidates().items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", clone(preprocessor)),
                ("model", estimator),
            ]
        )
        pipeline.fit(X_train, y_train)
        trained_models[model_name] = pipeline

    return trained_models


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Render a simple Markdown table without optional pandas dependencies."""
    rendered = df.copy()
    for column in rendered.select_dtypes(include=["float"]).columns:
        rendered[column] = rendered[column].map(lambda value: f"{value:.4f}")

    headers = list(rendered.columns)
    rows = rendered.astype(str).values.tolist()
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def save_models(models: dict[str, Pipeline], model_dir: str | Path = MODEL_DIR) -> None:
    """Persist trained model pipelines as pickle files."""
    model_dir = resolve_project_path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    for model_name, model in models.items():
        output_path = model_dir / MODEL_ARTIFACT_NAMES[model_name]
        with output_path.open("wb") as file:
            pickle.dump(model, file)


def create_comparison_table(comparison: pd.DataFrame) -> pd.DataFrame:
    """Create the report table focused on class-1 SLA breach metrics."""
    table = comparison.copy()
    table["Model"] = table["model"].map(MODEL_DISPLAY_NAMES)

    table = table.rename(
        columns={
            "accuracy": "Accuracy",
            "precision_class_1": "Precision Class 1",
            "recall_class_1": "Recall Class 1",
            "f1_class_1": "F1 Class 1",
            "roc_auc": "ROC-AUC",
            "pr_auc": "PR-AUC",
        }
    )

    return table[
        [
            "Model",
            "Accuracy",
            "Precision Class 1",
            "Recall Class 1",
            "F1 Class 1",
            "ROC-AUC",
            "PR-AUC",
        ]
    ]


def generate_markdown_report(
    comparison: pd.DataFrame,
    metrics: list[dict[str, Any]],
    y_train: pd.Series,
    y_test: pd.Series,
) -> str:
    """Create a Markdown baseline model comparison report."""
    train_rate = y_train.mean()
    test_rate = y_test.mean()
    best_row = comparison.sort_values(
        by=["recall_class_1", "pr_auc", "precision_class_1"],
        ascending=False,
    ).iloc[0]
    best_model = MODEL_DISPLAY_NAMES[best_row["model"]]
    comparison_table = create_comparison_table(comparison)

    lines = [
        "# Baseline Model Report",
        "",
        "## Dataset",
        "",
        f"- Source: `{display_project_path(DATA_PATH)}`",
        f"- Training rows: {len(y_train):,}",
        f"- Test rows: {len(y_test):,}",
        f"- Target: `{TARGET_COLUMN}`",
        f"- Train SLA breach rate: {train_rate:.2%}",
        f"- Test SLA breach rate: {test_rate:.2%}",
        f"- Test split: stratified {TEST_SIZE:.0%} holdout with random_state={RANDOM_STATE}",
        "",
        "## Feature Handling",
        "",
        "- `X` uses only the approved model features from `docs/feature_list_v1.md`.",
        "- ID columns and leakage columns are excluded from model input.",
        "- Numeric features use median imputation and standard scaling.",
        "- Categorical features use `Unknown` imputation and one-hot encoding with unknown-category handling.",
        "- `purchase_day_of_week` is treated as a categorical feature.",
        "",
        "## Saved Model Artifacts",
        "",
        "- `models/baseline_logistic_regression.pkl`",
        "- `models/baseline_decision_tree.pkl`",
        "- `models/baseline_random_forest.pkl`",
        "",
        "## Model Comparison",
        "",
        dataframe_to_markdown(comparison_table),
        "",
        f"Best baseline by class-1 recall, then PR-AUC, then class-1 precision: `{best_model}`.",
        "",
        "## Confusion Matrices",
        "",
    ]

    for metric in metrics:
        lines.extend(
            [
                f"### {MODEL_DISPLAY_NAMES[metric['model']]}",
                "",
                "| Actual / Predicted | Predicted 0 | Predicted 1 |",
                "| --- | ---: | ---: |",
                f"| Actual 0 | {metric['true_negatives']} | {metric['false_positives']} |",
                f"| Actual 1 | {metric['false_negatives']} | {metric['true_positives']} |",
                "",
            ]
        )

    lines.extend(
        [
            "## Classification Reports",
            "",
        ]
    )

    for metric in metrics:
        lines.extend(
            [
                f"### {MODEL_DISPLAY_NAMES[metric['model']]}",
                "",
                "```text",
                metric["classification_report"].strip(),
                "```",
                "",
            ]
        )

    return "\n".join(lines)


def save_report(report: str, report_path: str | Path = REPORT_PATH) -> None:
    """Persist the Markdown model comparison report."""
    report_path = resolve_project_path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")


def run_baseline_training(
    input_path: str | Path = DATA_PATH,
    model_dir: str | Path = MODEL_DIR,
    report_path: str | Path = REPORT_PATH,
) -> pd.DataFrame:
    """Run the complete baseline modeling workflow."""
    df = load_feature_dataset(input_path)
    X, y = separate_features_and_target(df)
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    preprocessor = build_preprocessor(X_train)
    models = train_models(X_train, y_train, preprocessor)

    metrics = [
        evaluate_classifier(model_name, model, X_test, y_test)
        for model_name, model in models.items()
    ]
    comparison = metrics_to_frame(metrics)

    save_models(models, model_dir)
    report = generate_markdown_report(comparison, metrics, y_train, y_test)
    save_report(report, report_path)

    return comparison


def main() -> None:
    """Run baseline training and print the model comparison table."""
    comparison = run_baseline_training()
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    main()
