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


def metrics_to_frame(metrics: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert model metric dictionaries into a comparison table."""
    columns = [
        "model",
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
    return pd.DataFrame(metrics)[columns]
