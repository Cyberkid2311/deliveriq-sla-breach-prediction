from __future__ import annotations

from pathlib import Path
import pickle
from typing import Any

import pandas as pd
import warnings
from sklearn.pipeline import Pipeline

try:
    from src.models.evaluate_model import (
        evaluate_classifier,
        evaluate_threshold_grid,
        metrics_to_frame,
        select_recall_first_threshold,
    )
    from src.models.model_selection import (
        format_risk_bucket_logic,
        select_final_model,
    )
    from src.models.train_baseline import (
        DATA_PATH,
        MODEL_DIR,
        APPROVED_MODEL_FEATURES,
        PROJECT_ROOT,
        TARGET_COLUMN,
        TEST_SIZE,
        build_model_candidates as build_baseline_candidates,
        build_preprocessor as build_baseline_preprocessor,
        dataframe_to_markdown,
        display_project_path,
        load_feature_dataset,
        resolve_project_path,
        split_train_test,
    )
    from src.models.train_optimized import (
        build_dense_ordinal_preprocessor,
        separate_optimized_features_and_target,
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
    from src.models.model_selection import (
        format_risk_bucket_logic,
        select_final_model,
    )
    from src.models.train_baseline import (
        DATA_PATH,
        MODEL_DIR,
        APPROVED_MODEL_FEATURES,
        PROJECT_ROOT,
        TARGET_COLUMN,
        TEST_SIZE,
        build_model_candidates as build_baseline_candidates,
        build_preprocessor as build_baseline_preprocessor,
        dataframe_to_markdown,
        display_project_path,
        load_feature_dataset,
        resolve_project_path,
        split_train_test,
    )
    from src.models.train_optimized import (
        build_dense_ordinal_preprocessor,
        separate_optimized_features_and_target,
    )


ADVANCED_REPORT_PATH = PROJECT_ROOT / "reports/advanced_model_report.md"
MODEL_SELECTION_NOTES_PATH = PROJECT_ROOT / "docs/day5_model_selection_notes.md"
DAY5_OPTIMIZATION_REPORT_PATH = PROJECT_ROOT / "reports/day5_model_optimization_report.md"
DAY5_THRESHOLD_REPORT_PATH = PROJECT_ROOT / "reports/day5_threshold_tuning_report.md"
FINAL_MODEL_PATH = MODEL_DIR / "final_model.pkl"

BASELINE_DISPLAY_NAMES = {
    "logistic_regression": "Logistic Regression",
    "decision_tree": "Decision Tree",
    "random_forest": "Random Forest",
}

ADVANCED_DISPLAY_NAMES = {
    "lightgbm": "LightGBM Classifier",
    "xgboost": "XGBoost Classifier",
}

DISPLAY_NAMES = {
    **BASELINE_DISPLAY_NAMES,
    **ADVANCED_DISPLAY_NAMES,
}

MODEL_NOTES = {
    "logistic_regression": "Baseline",
    "decision_tree": "Baseline",
    "random_forest": "Baseline",
    "lightgbm": "Advanced final model candidate",
    "xgboost": "Advanced optional comparison model",
}


def train_baseline_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> dict[str, Any]:
    """Train the Day 4 baseline candidates on the same split."""
    preprocessor = build_baseline_preprocessor(X_train)
    models = {}
    for model_name, estimator in build_baseline_candidates().items():
        from sklearn.base import clone
        from sklearn.pipeline import Pipeline

        models[model_name] = Pipeline(
            steps=[
                ("preprocessor", clone(preprocessor)),
                ("model", estimator),
            ]
        )
        models[model_name].fit(X_train, y_train)
    return models


def calculate_scale_pos_weight(y_train: pd.Series) -> float:
    """Calculate imbalance weight for gradient boosting classifiers."""
    positives = int((y_train == 1).sum())
    negatives = int((y_train == 0).sum())
    if positives == 0:
        return 1.0
    return negatives / positives


def train_advanced_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> dict[str, Any]:
    """Train the requested LightGBM and XGBoost advanced candidates."""
    try:
        from lightgbm import LGBMClassifier
        from xgboost import XGBClassifier
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(
            "LightGBM and XGBoost are required for Day 5 advanced training. "
            "Install them with `pip install lightgbm xgboost`."
        ) from error

    scale_pos_weight = calculate_scale_pos_weight(y_train)
    models = {
        "lightgbm": Pipeline(
            steps=[
                ("preprocessor", build_dense_ordinal_preprocessor(X_train)),
                (
                    "model",
                    LGBMClassifier(
                        class_weight="balanced",
                        learning_rate=0.05,
                        max_depth=8,
                        n_estimators=300,
                        num_leaves=31,
                        objective="binary",
                        random_state=42,
                        verbosity=-1,
                    ),
                ),
            ]
        ),
        "xgboost": Pipeline(
            steps=[
                ("preprocessor", build_dense_ordinal_preprocessor(X_train)),
                (
                    "model",
                    XGBClassifier(
                        eval_metric="logloss",
                        learning_rate=0.05,
                        max_depth=6,
                        n_estimators=300,
                        n_jobs=1,
                        random_state=42,
                        scale_pos_weight=scale_pos_weight,
                        subsample=0.9,
                        colsample_bytree=0.9,
                    ),
                ),
            ]
        ),
    }

    for model in models.values():
        model.fit(X_train, y_train)
    return models


def create_model_comparison_table(metrics: pd.DataFrame) -> pd.DataFrame:
    """Create the report-ready baseline and advanced model comparison table."""
    table = metrics.copy()
    table["Model"] = table["model"].map(DISPLAY_NAMES)
    table["Notes"] = table["model"].map(MODEL_NOTES)
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
            "Notes",
        ]
    ]


def generate_advanced_model_report(
    metrics: pd.DataFrame,
    selected_thresholds: pd.DataFrame,
    final_model_name: str,
    final_row: pd.Series,
) -> str:
    """Create the business-friendly Day 5 advanced model report."""
    comparison_table = create_model_comparison_table(metrics)
    best_recall_model = DISPLAY_NAMES[
        metrics.sort_values("recall_class_1", ascending=False).iloc[0]["model"]
    ]
    best_balance_model = DISPLAY_NAMES[
        metrics.sort_values("f1_class_1", ascending=False).iloc[0]["model"]
    ]

    selected_table = selected_thresholds.copy()
    selected_table["Model"] = selected_table["model"].map(DISPLAY_NAMES)
    selected_table = selected_table.rename(
        columns={
            "threshold": "Threshold",
            "precision_class_1": "Precision Class 1",
            "recall_class_1": "Recall Class 1",
            "f1_class_1": "F1 Class 1",
            "false_positives": "False Positives",
            "false_negatives": "False Negatives",
        }
    )
    selected_table = selected_table[
        [
            "Model",
            "Threshold",
            "Precision Class 1",
            "Recall Class 1",
            "F1 Class 1",
            "False Positives",
            "False Negatives",
        ]
    ]

    lines = [
        "# Advanced Model Report",
        "",
        "## Business Summary",
        "",
        f"The selected final model is `{DISPLAY_NAMES[final_model_name]}`.",
        "The selection prioritizes catching SLA breaches, then precision, F1-score, PR-AUC, and ROC-AUC.",
        f"The best default-threshold recall model is `{best_recall_model}`.",
        f"The best default-threshold precision-recall balance by F1 is `{best_balance_model}`.",
        "",
        "Advanced models were implemented with LightGBM and XGBoost as requested, then compared against the three Day 4 baselines on the same held-out test split.",
        "",
        "## Model Comparison",
        "",
        dataframe_to_markdown(comparison_table),
        "",
        "## Recall-First Threshold Review",
        "",
        dataframe_to_markdown(selected_table),
        "",
        "## Final Model Selection",
        "",
        f"- Final model: `{DISPLAY_NAMES[final_model_name]}`",
        f"- Saved artifact: `models/final_model.pkl`",
        f"- Default operating threshold: {float(final_row['threshold']):.2f}",
        f"- Recall class 1: {float(final_row['recall_class_1']):.4f}",
        f"- Precision class 1: {float(final_row['precision_class_1']):.4f}",
        f"- F1 class 1: {float(final_row['f1_class_1']):.4f}",
        f"- PR-AUC: {float(final_row['pr_auc']):.4f}",
        "",
        "## Risk Bucket Logic",
        "",
        format_risk_bucket_logic(),
        "",
        "## Implemented Model Lineup",
        "",
        "- Baseline 1: Logistic Regression",
        "- Baseline 2: Decision Tree",
        "- Baseline 3: Random Forest",
        "- Advanced 1: LightGBM Classifier",
        "- Advanced 2: XGBoost Classifier",
        "",
    ]
    return "\n".join(lines)


def generate_threshold_report(threshold_metrics: pd.DataFrame) -> str:
    """Create a full threshold tuning report for all five requested models."""
    report_table = threshold_metrics.copy()
    report_table["Model"] = report_table["model"].map(DISPLAY_NAMES)
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

    return "\n".join(
        [
            "# Day 5 Threshold Tuning Report",
            "",
            "Thresholds are evaluated from 0.05 to 0.95 for the SLA breach class across the requested five-model lineup.",
            "",
            dataframe_to_markdown(report_table),
            "",
        ]
    )


def generate_model_selection_notes(
    metrics: pd.DataFrame,
    final_model_name: str,
    final_row: pd.Series,
) -> str:
    """Create the lead ML owner Day 5 model selection note."""
    baseline_best = metrics[
        metrics["model"].isin(BASELINE_DISPLAY_NAMES)
    ].sort_values(
        by=["recall_class_1", "precision_class_1", "f1_class_1", "pr_auc"],
        ascending=False,
    ).iloc[0]

    lines = [
        "# Day 5 Model Selection Notes",
        "",
        "## Validation",
        "",
        f"- Source dataset: `{display_project_path(DATA_PATH)}`",
        f"- Target: `{TARGET_COLUMN}`",
        f"- Split: stratified {TEST_SIZE:.0%} holdout using the same Day 4 logic.",
        "- Preprocessing is contained inside sklearn pipelines.",
        "- Final model inputs use approved pre-delivery features only.",
        "",
        "## Final Decision",
        "",
        f"- Selected model: `{DISPLAY_NAMES[final_model_name]}`",
        f"- Final artifact: `models/final_model.pkl`",
        f"- Selected threshold: {float(final_row['threshold']):.2f}",
        "",
        "The final model is selected by the project priority order: recall, precision, F1-score, PR-AUC, ROC-AUC, stability, explainability, and ease of deployment.",
        "",
        "## Baseline Versus Final Model",
        "",
        f"- Best Day 4 baseline by recall: `{DISPLAY_NAMES[baseline_best['model']]}` with recall {baseline_best['recall_class_1']:.4f}.",
        f"- Final model threshold recall: {float(final_row['recall_class_1']):.4f}.",
        f"- Final model threshold precision: {float(final_row['precision_class_1']):.4f}.",
        f"- Final model false negatives: {int(final_row['false_negatives'])}.",
        f"- Final model false positives: {int(final_row['false_positives'])}.",
        "",
        "## Threshold Strategy",
        "",
        "The project uses a tuned probability threshold rather than relying only on 0.50. Lower thresholds catch more risky orders but create more false alerts. The selected threshold is intended for recall-first operations.",
        "",
        "## Risk Bucket Logic",
        "",
        format_risk_bucket_logic(),
        "",
        "## Day 6 Readiness",
        "",
        "The model is ready for Day 6 risk scoring, explainability, and dashboard work.",
        "",
    ]
    return "\n".join(lines)


def save_pickle(model: Any, output_path: str | Path) -> None:
    """Save a pickle artifact."""
    output_path = resolve_project_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as file:
        pickle.dump(model, file)


def save_text(text: str, output_path: str | Path) -> None:
    """Save text output."""
    output_path = resolve_project_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def run_training(
    input_path: str | Path = DATA_PATH,
    final_model_path: str | Path = FINAL_MODEL_PATH,
) -> pd.DataFrame:
    """Train baseline and advanced models, select final model, and save reports."""
    warnings.filterwarnings(
        "ignore",
        message="X does not have valid feature names",
        category=UserWarning,
    )
    df = load_feature_dataset(input_path)
    X, y = separate_optimized_features_and_target(df)
    X_train, X_test, y_train, y_test = split_train_test(X, y)

    baseline_models = train_baseline_models(
        X_train[APPROVED_MODEL_FEATURES],
        y_train,
    )
    advanced_models = train_advanced_models(X_train, y_train)

    all_models = {**baseline_models, **advanced_models}
    eval_inputs = {
        **{
            model_name: X_test[APPROVED_MODEL_FEATURES]
            for model_name in baseline_models
        },
        **{model_name: X_test for model_name in advanced_models},
    }

    metrics = metrics_to_frame(
        [
            evaluate_classifier(model_name, model, eval_inputs[model_name], y_test)
            for model_name, model in all_models.items()
        ]
    )
    threshold_metrics = pd.concat(
        [
            evaluate_threshold_grid(model_name, model, eval_inputs[model_name], y_test)
            for model_name, model in all_models.items()
        ],
        ignore_index=True,
    )
    selected_thresholds = pd.DataFrame(
        [
            select_recall_first_threshold(
                threshold_metrics[threshold_metrics["model"] == model_name]
            )
            for model_name in all_models
        ]
    )
    final_model_name, final_model, final_row = select_final_model(
        selected_thresholds,
        all_models,
    )

    save_pickle(final_model, final_model_path)
    save_text(
        generate_advanced_model_report(
            metrics,
            selected_thresholds,
            final_model_name,
            final_row,
        ),
        ADVANCED_REPORT_PATH,
    )
    save_text(
        generate_advanced_model_report(
            metrics,
            selected_thresholds,
            final_model_name,
            final_row,
        ),
        DAY5_OPTIMIZATION_REPORT_PATH,
    )
    save_text(
        generate_threshold_report(threshold_metrics),
        DAY5_THRESHOLD_REPORT_PATH,
    )
    save_text(
        generate_model_selection_notes(metrics, final_model_name, final_row),
        MODEL_SELECTION_NOTES_PATH,
    )

    return selected_thresholds


def main() -> None:
    """Run Day 5 advanced training and model selection."""
    selected_thresholds = run_training()
    print(selected_thresholds.to_string(index=False))


if __name__ == "__main__":
    main()
