from __future__ import annotations

import os
from pathlib import Path
import pickle
from typing import Any

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

try:
    from src.models.evaluate_model import (
        evaluate_classifier,
        evaluate_threshold_grid,
        metrics_to_frame,
        select_recall_first_threshold,
    )
    from src.models.train_baseline import (
        DATA_PATH,
        MODEL_DIR,
        PROJECT_ROOT,
        RANDOM_STATE,
        TARGET_COLUMN,
        TEST_SIZE,
        dataframe_to_markdown,
        display_project_path,
        load_feature_dataset,
        resolve_project_path,
        split_train_test,
    )
except ModuleNotFoundError:
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.models.evaluate_model import (
        evaluate_classifier,
        evaluate_threshold_grid,
        metrics_to_frame,
        select_recall_first_threshold,
    )
    from src.models.train_baseline import (
        DATA_PATH,
        MODEL_DIR,
        PROJECT_ROOT,
        RANDOM_STATE,
        TARGET_COLUMN,
        TEST_SIZE,
        dataframe_to_markdown,
        display_project_path,
        load_feature_dataset,
        resolve_project_path,
        split_train_test,
    )


OPTIMIZATION_REPORT_PATH = PROJECT_ROOT / "reports/day5_model_optimization_report.md"
THRESHOLD_REPORT_PATH = PROJECT_ROOT / "reports/day5_threshold_tuning_report.md"

OPTIMIZED_MODEL_FEATURES = [
    "purchase_day_of_week",
    "purchase_hour",
    "is_weekend_order",
    "estimated_delivery_days",
    "estimated_delivery_days_bucket",
    "customer_state",
    "customer_city",
    "seller_state",
    "seller_city",
    "seller_customer_same_state",
    "seller_customer_same_city",
    "seller_customer_same_zip_prefix",
    "seller_customer_state_pair",
    "seller_customer_city_pair",
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
    "freight_value",
    "avg_freight_value",
    "freight_value_bucket",
    "price",
    "avg_price",
    "item_count",
    "product_count",
    "product_count_bucket",
    "seller_count",
    "seller_count_bucket",
    "product_category_count",
    "item_count_bucket",
    "price_per_item",
    "freight_per_item",
    "price_bucket",
    "freight_per_item_bucket",
]

NUMERICAL_FEATURES = [
    "purchase_hour",
    "is_weekend_order",
    "estimated_delivery_days",
    "seller_customer_same_state",
    "seller_customer_same_city",
    "seller_customer_same_zip_prefix",
    "product_weight_g",
    "product_weight_kg",
    "total_product_weight_g",
    "total_product_weight_kg",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "product_volume_cm3",
    "total_product_volume_cm3",
    "freight_value",
    "avg_freight_value",
    "price",
    "avg_price",
    "item_count",
    "product_count",
    "seller_count",
    "product_category_count",
    "price_per_item",
    "freight_per_item",
]

CATEGORICAL_FEATURES = [
    "purchase_day_of_week",
    "estimated_delivery_days_bucket",
    "customer_state",
    "customer_city",
    "seller_state",
    "seller_city",
    "seller_customer_state_pair",
    "seller_customer_city_pair",
    "product_category_name",
    "product_weight_bucket",
    "freight_value_bucket",
    "product_count_bucket",
    "seller_count_bucket",
    "item_count_bucket",
    "price_bucket",
    "freight_per_item_bucket",
]

MODEL_DISPLAY_NAMES = {
    "optimized_logistic_regression": "Optimized Logistic Regression",
    "optimized_random_forest": "Optimized Random Forest",
    "hist_gradient_boosting": "HistGradientBoosting",
}

MODEL_ARTIFACT_NAMES = {
    "optimized_logistic_regression": "day5_optimized_logistic_regression.pkl",
    "optimized_random_forest": "day5_optimized_random_forest.pkl",
    "hist_gradient_boosting": "day5_hist_gradient_boosting.pkl",
}


def separate_optimized_features_and_target(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Create X/y for the Day 5 optimized feature set."""
    missing_features = sorted(set(OPTIMIZED_MODEL_FEATURES) - set(df.columns))
    if missing_features:
        raise ValueError(
            "Missing optimized model features:\n" + "\n".join(missing_features)
        )

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    X = df[OPTIMIZED_MODEL_FEATURES].copy()
    y = df[TARGET_COLUMN].astype("int64")

    invalid_target_values = set(y.dropna().unique()) - {0, 1}
    if invalid_target_values:
        raise ValueError(f"Invalid target values: {invalid_target_values}")

    return X, y


def _validate_feature_assignments(X: pd.DataFrame) -> None:
    assigned_features = set(NUMERICAL_FEATURES + CATEGORICAL_FEATURES)
    unassigned_features = sorted(set(X.columns) - assigned_features)
    if unassigned_features:
        raise ValueError(
            "Features missing preprocessing assignment:\n"
            + "\n".join(unassigned_features)
        )


def build_sparse_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Build one-hot preprocessing for linear and forest candidates."""
    _validate_feature_assignments(X)
    numeric_features = [column for column in NUMERICAL_FEATURES if column in X.columns]
    categorical_features = [
        column for column in CATEGORICAL_FEATURES if column in X.columns
    ]

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


def build_dense_ordinal_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Build dense ordinal preprocessing for histogram gradient boosting."""
    _validate_feature_assignments(X)
    numeric_features = [column for column in NUMERICAL_FEATURES if column in X.columns]
    categorical_features = [
        column for column in CATEGORICAL_FEATURES if column in X.columns
    ]

    numeric_pipeline = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median"))]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            (
                "ordinal",
                OrdinalEncoder(
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
        sparse_threshold=0.0,
    )


def build_model_candidates(X_train: pd.DataFrame) -> dict[str, Pipeline]:
    """Define Day 5 optimized sklearn model candidates."""
    sparse_preprocessor = build_sparse_preprocessor(X_train)
    dense_preprocessor = build_dense_ordinal_preprocessor(X_train)

    return {
        "optimized_logistic_regression": Pipeline(
            steps=[
                ("preprocessor", sparse_preprocessor),
                (
                    "model",
                    LogisticRegression(
                        C=0.5,
                        class_weight="balanced",
                        max_iter=2000,
                        random_state=RANDOM_STATE,
                        solver="liblinear",
                    ),
                ),
            ]
        ),
        "optimized_random_forest": Pipeline(
            steps=[
                ("preprocessor", sparse_preprocessor),
                (
                    "model",
                    RandomForestClassifier(
                        class_weight="balanced_subsample",
                        max_depth=24,
                        min_samples_leaf=25,
                        n_estimators=200,
                        n_jobs=1,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "hist_gradient_boosting": Pipeline(
            steps=[
                ("preprocessor", dense_preprocessor),
                (
                    "model",
                    HistGradientBoostingClassifier(
                        l2_regularization=0.05,
                        learning_rate=0.06,
                        max_iter=200,
                        max_leaf_nodes=31,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
    }


def train_models(X_train: pd.DataFrame, y_train: pd.Series) -> dict[str, Pipeline]:
    """Fit all Day 5 optimized candidates."""
    models = build_model_candidates(X_train)
    for model in models.values():
        model.fit(X_train, y_train)
    return models


def create_selected_thresholds_table(selected_thresholds: pd.DataFrame) -> pd.DataFrame:
    """Create the compact selected-threshold report table."""
    table = selected_thresholds.copy()
    table["Model"] = table["model"].map(MODEL_DISPLAY_NAMES)
    table = table.rename(
        columns={
            "threshold": "Threshold",
            "accuracy": "Accuracy",
            "precision_class_1": "Precision Class 1",
            "recall_class_1": "Recall Class 1",
            "f1_class_1": "F1 Class 1",
            "roc_auc": "ROC-AUC",
            "pr_auc": "PR-AUC",
            "false_positives": "False Positives",
            "false_negatives": "False Negatives",
            "true_positives": "True Positives",
        }
    )
    return table[
        [
            "Model",
            "Threshold",
            "Precision Class 1",
            "Recall Class 1",
            "F1 Class 1",
            "PR-AUC",
            "ROC-AUC",
            "False Positives",
            "False Negatives",
            "True Positives",
        ]
    ]


def create_default_metrics_table(default_metrics: pd.DataFrame) -> pd.DataFrame:
    """Create the default-threshold model comparison table."""
    table = default_metrics.copy()
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
            "PR-AUC",
            "ROC-AUC",
        ]
    ]


def generate_optimization_report(
    default_metrics: pd.DataFrame,
    selected_thresholds: pd.DataFrame,
    best_model_name: str,
    y_train: pd.Series,
    y_test: pd.Series,
) -> str:
    """Create the Day 5 optimized model comparison report."""
    default_table = create_default_metrics_table(default_metrics)
    selected_table = create_selected_thresholds_table(selected_thresholds)
    best_row = selected_thresholds[selected_thresholds["model"] == best_model_name].iloc[0]

    lines = [
        "# Day 5 Model Optimization Report",
        "",
        "## Dataset",
        "",
        f"- Source: `{display_project_path(DATA_PATH)}`",
        f"- Training rows: {len(y_train):,}",
        f"- Test rows: {len(y_test):,}",
        f"- Target: `{TARGET_COLUMN}`",
        f"- Train SLA breach rate: {y_train.mean():.2%}",
        f"- Test SLA breach rate: {y_test.mean():.2%}",
        f"- Test split: stratified {TEST_SIZE:.0%} holdout with random_state={RANDOM_STATE}",
        "",
        "## Optimization Approach",
        "",
        "- Added model-safe delivery estimate, route, and order intensity features.",
        "- Trained sklearn-only optimized candidates.",
        "- Evaluated probability thresholds from 0.05 to 0.95.",
        "- Selected thresholds using recall first after basic precision and false-positive guardrails.",
        "",
        "## Default Threshold Model Comparison",
        "",
        dataframe_to_markdown(default_table),
        "",
        "## Selected Recall-First Thresholds",
        "",
        dataframe_to_markdown(selected_table),
        "",
        "## Recommended Operational Model",
        "",
        f"- Model: `{MODEL_DISPLAY_NAMES[best_model_name]}`",
        f"- Threshold: {best_row['threshold']:.2f}",
        f"- Recall class 1: {best_row['recall_class_1']:.4f}",
        f"- Precision class 1: {best_row['precision_class_1']:.4f}",
        f"- False negatives: {int(best_row['false_negatives'])}",
        f"- False positives: {int(best_row['false_positives'])}",
        "",
    ]

    return "\n".join(lines)


def generate_threshold_report(threshold_metrics: pd.DataFrame) -> str:
    """Create the full Day 5 threshold tuning report."""
    report_table = threshold_metrics.copy()
    report_table["Model"] = report_table["model"].map(MODEL_DISPLAY_NAMES)
    report_table = report_table.rename(
        columns={
            "threshold": "Threshold",
            "precision_class_1": "Precision Class 1",
            "recall_class_1": "Recall Class 1",
            "f1_class_1": "F1 Class 1",
            "pr_auc": "PR-AUC",
            "roc_auc": "ROC-AUC",
            "false_positives": "False Positives",
            "false_negatives": "False Negatives",
            "true_positives": "True Positives",
        }
    )
    report_table = report_table[
        [
            "Model",
            "Threshold",
            "Precision Class 1",
            "Recall Class 1",
            "F1 Class 1",
            "PR-AUC",
            "ROC-AUC",
            "False Positives",
            "False Negatives",
            "True Positives",
        ]
    ]

    lines = [
        "# Day 5 Threshold Tuning Report",
        "",
        "Thresholds are evaluated from 0.05 to 0.95 for the SLA breach class.",
        "The operational recommendation in the optimization report uses recall-first ranking with basic precision and false-positive guardrails.",
        "",
        dataframe_to_markdown(report_table),
        "",
    ]
    return "\n".join(lines)


def save_models(
    models: dict[str, Pipeline],
    best_model_name: str,
    model_dir: str | Path = MODEL_DIR,
) -> None:
    """Persist Day 5 model candidates and the selected optimized model."""
    model_dir = resolve_project_path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    for model_name, model in models.items():
        output_path = model_dir / MODEL_ARTIFACT_NAMES[model_name]
        with output_path.open("wb") as file:
            pickle.dump(model, file)

    best_output_path = model_dir / "day5_optimized_best_model.pkl"
    with best_output_path.open("wb") as file:
        pickle.dump(models[best_model_name], file)


def save_report(report: str, report_path: str | Path) -> None:
    """Persist a Markdown report."""
    report_path = resolve_project_path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")


def run_optimized_training(
    input_path: str | Path = DATA_PATH,
    model_dir: str | Path = MODEL_DIR,
    optimization_report_path: str | Path = OPTIMIZATION_REPORT_PATH,
    threshold_report_path: str | Path = THRESHOLD_REPORT_PATH,
) -> pd.DataFrame:
    """Run the complete Day 5 optimized modeling workflow."""
    df = load_feature_dataset(input_path)
    X, y = separate_optimized_features_and_target(df)
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    models = train_models(X_train, y_train)

    default_metrics = metrics_to_frame(
        [
            evaluate_classifier(model_name, model, X_test, y_test)
            for model_name, model in models.items()
        ]
    )
    threshold_metrics = pd.concat(
        [
            evaluate_threshold_grid(model_name, model, X_test, y_test)
            for model_name, model in models.items()
        ],
        ignore_index=True,
    )
    selected_thresholds = pd.DataFrame(
        [
            select_recall_first_threshold(
                threshold_metrics[threshold_metrics["model"] == model_name]
            )
            for model_name in models
        ]
    )
    best_model_name = (
        selected_thresholds.sort_values(
            by=["recall_class_1", "pr_auc", "precision_class_1", "f1_class_1"],
            ascending=False,
        )
        .iloc[0]["model"]
    )

    save_models(models, best_model_name, model_dir)
    save_report(
        generate_optimization_report(
            default_metrics,
            selected_thresholds,
            best_model_name,
            y_train,
            y_test,
        ),
        optimization_report_path,
    )
    save_report(generate_threshold_report(threshold_metrics), threshold_report_path)

    return selected_thresholds


def main() -> None:
    """Run Day 5 optimized training and print selected thresholds."""
    selected_thresholds = run_optimized_training()
    print(selected_thresholds.to_string(index=False))


if __name__ == "__main__":
    main()
