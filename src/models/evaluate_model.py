from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def get_positive_class_scores(model: Any, X_test: pd.DataFrame) -> np.ndarray:
    """Return positive-class scores for classifiers with probabilities or margins."""
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X_test)[:, 1]

    if hasattr(model, "decision_function"):
        return model.decision_function(X_test)

    raise ValueError("Model must expose predict_proba or decision_function.")


def evaluate_classifier(
    model_name: str,
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, Any]:
    """Evaluate a fitted binary classifier on the held-out test set."""
    y_pred = model.predict(X_test)
    y_score = get_positive_class_scores(model, X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=[0, 1]).ravel()

    return {
        "model": model_name,
        "accuracy": accuracy_score(y_test, y_pred),
        "precision_class_1": precision_score(y_test, y_pred, zero_division=0),
        "recall_class_1": recall_score(y_test, y_pred, zero_division=0),
        "f1_class_1": f1_score(y_test, y_pred, zero_division=0),
        "pr_auc": average_precision_score(y_test, y_score),
        "roc_auc": roc_auc_score(y_test, y_score),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "classification_report": classification_report(
            y_test,
            y_pred,
            labels=[0, 1],
            target_names=["on_time", "sla_breached"],
            zero_division=0,
        ),
    }


def evaluate_scores_at_threshold(
    model_name: str,
    y_true: pd.Series,
    y_score: np.ndarray,
    threshold: float,
) -> dict[str, Any]:
    """Evaluate binary classifier scores at a chosen positive-class threshold."""
    y_pred = (y_score >= threshold).astype("int64")
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    return {
        "model": model_name,
        "threshold": threshold,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_class_1": precision_score(y_true, y_pred, zero_division=0),
        "recall_class_1": recall_score(y_true, y_pred, zero_division=0),
        "f1_class_1": f1_score(y_true, y_pred, zero_division=0),
        "pr_auc": average_precision_score(y_true, y_score),
        "roc_auc": roc_auc_score(y_true, y_score),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }


def evaluate_threshold_grid(
    model_name: str,
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    thresholds: np.ndarray | None = None,
) -> pd.DataFrame:
    """Evaluate a fitted classifier across a probability threshold grid."""
    if thresholds is None:
        thresholds = np.round(np.arange(0.05, 1.0, 0.05), 2)

    y_score = get_positive_class_scores(model, X_test)
    rows = [
        evaluate_scores_at_threshold(model_name, y_test, y_score, float(threshold))
        for threshold in thresholds
    ]
    return pd.DataFrame(rows)


def select_recall_first_threshold(
    threshold_metrics: pd.DataFrame,
    min_precision: float = 0.10,
    max_false_positive_rate: float = 0.80,
) -> pd.Series:
    """Select a recall-first threshold that respects basic operational guardrails."""
    total_negatives = (
        threshold_metrics["true_negatives"].iloc[0]
        + threshold_metrics["false_positives"].iloc[0]
    )
    eligible_thresholds = threshold_metrics[
        (threshold_metrics["precision_class_1"] >= min_precision)
        & (
            threshold_metrics["false_positives"]
            <= total_negatives * max_false_positive_rate
        )
    ]

    if eligible_thresholds.empty:
        eligible_thresholds = threshold_metrics

    return eligible_thresholds.sort_values(
        by=[
            "recall_class_1",
            "precision_class_1",
            "f1_class_1",
            "false_positives",
        ],
        ascending=[False, False, False, True],
    ).iloc[0]


def select_f1_first_threshold(threshold_metrics: pd.DataFrame) -> pd.Series:
    """Select the threshold with the strongest class-1 F1 score."""
    return threshold_metrics.sort_values(
        by=[
            "f1_class_1",
            "recall_class_1",
            "precision_class_1",
            "false_positives",
        ],
        ascending=[False, False, False, True],
    ).iloc[0]


def select_precision_floor_threshold(
    threshold_metrics: pd.DataFrame,
    min_precision: float,
) -> pd.Series:
    """Maximize recall subject to a minimum class-1 precision floor."""
    eligible_thresholds = threshold_metrics[
        threshold_metrics["precision_class_1"] >= min_precision
    ]

    if eligible_thresholds.empty:
        eligible_thresholds = threshold_metrics

    return eligible_thresholds.sort_values(
        by=[
            "recall_class_1",
            "precision_class_1",
            "f1_class_1",
            "false_positives",
        ],
        ascending=[False, False, False, True],
    ).iloc[0]


def metrics_to_frame(metrics: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert model metric dictionaries into a comparison table."""
    columns = [
        "model",
        "threshold",
        "accuracy",
        "precision_class_1",
        "recall_class_1",
        "f1_class_1",
        "roc_auc",
        "pr_auc",
        "true_negatives",
        "false_positives",
        "false_negatives",
        "true_positives",
    ]
    frame = pd.DataFrame(metrics)
    available_columns = [column for column in columns if column in frame.columns]
    return frame[available_columns]
