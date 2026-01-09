import joblib
import numpy as np
import os

MODEL_PATH = "nutrition_risk_model.pkl"

model = joblib.load(MODEL_PATH)

LABELS = ["LOW", "MEDIUM", "HIGH"]

def predict_risk(features):
    X = np.array([[
        features["avg_iron"],
        features["avg_calcium"],
        features["avg_protein"],
        features["consistency"]
    ]])

    probabilities = model.predict_proba(X)[0]
    idx = probabilities.argmax()

    return {
        "risk_level": LABELS[idx],
        "confidence": round(float(probabilities[idx]), 2)
    }
