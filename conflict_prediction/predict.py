"""
AuraSCM - Conflict Prediction Module
--------------------------------------
Trains a lightweight, explainable ML classifier (Logistic Regression)
on merge-history features to predict whether an incoming merge is
"risky" -- i.e. likely to introduce a semantic conflict or break a
dependent function.

This is a genuinely trained model (not a hardcoded rule) so it improves
as more real merge-history data (data/merge_history.csv) is collected.
"""

import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

MODEL_PATH = os.path.join(os.path.dirname(__file__), "conflict_model.joblib")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "merge_history.csv")

FEATURE_COLS = ["lines_changed", "functions_touched", "dependency_depth",
                 "signature_changed", "token_overlap_ratio"]


def train_model(data_path: str = DATA_PATH, save_path: str = MODEL_PATH):
    df = pd.read_csv(data_path)
    X = df[FEATURE_COLS]
    y = df["risky_merge"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model trained. Test accuracy: {acc:.2%}")
    print(classification_report(y_test, preds, target_names=["safe", "risky"]))

    joblib.dump(model, save_path)
    print(f"Saved model to {save_path}")
    return model


def load_model(path: str = MODEL_PATH):
    if not os.path.exists(path):
        return train_model()
    return joblib.load(path)


def predict_risk(features: dict, model=None) -> dict:
    """
    features example:
      {
        "lines_changed": 25,
        "functions_touched": 2,
        "dependency_depth": 1,
        "signature_changed": 0,
        "token_overlap_ratio": 0.65
      }
    """
    if model is None:
        model = load_model()
    row = pd.DataFrame([features])[FEATURE_COLS]
    prob_risky = model.predict_proba(row)[0][1]
    label = "RISKY" if prob_risky >= 0.5 else "SAFE"
    return {"prediction": label, "risk_probability": round(float(prob_risky), 3)}


if __name__ == "__main__":
    model = train_model()

    # Simulate a prediction for the calculate_total() conflict we found
    # via the semantic engine + dependency graph (dependency_depth=1,
    # signature unchanged, moderate logic divergence).
    example = {
        "lines_changed": 3,
        "functions_touched": 1,
        "dependency_depth": 1,
        "signature_changed": 0,
        "token_overlap_ratio": 0.65,
    }
    result = predict_risk(example, model)
    print(f"\nExample prediction for `calculate_total` merge: {result}")
