import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from week1_signal_design.signal_design import build_signals

signals = build_signals()


signals["latency_norm"] = signals["avg_latency"] / signals["avg_latency"].max()
signals["instability_score"] = (
    0.6 * signals["error_rate"] +
    0.4 * signals["slow_rate"]
)
signals["risk_weighted"] = (
    signals["instability_score"] *
    signals["request_count"]
)

feature_cols = [
    "latency_norm",
    "instability_score",
    "risk_weighted"
]

X = signals[feature_cols]
y = signals["high_risk"]  # from Day 1

signals["high_risk"] = (
    (signals["error_rate"] > 0.3) |
    (signals["slow_rate"] > 0.4)
).astype(int)


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression()
model.fit(X_scaled, y)

signals["predicted_risk"] = model.predict(X_scaled)
signals["risk_probability"] = model.predict_proba(X_scaled)[:, 1]

print(signals[[
    "latency_norm",
    "instability_score",
    "risk_weighted",
    "high_risk",
    "predicted_risk",
    "risk_probability"
]])

coefficients = pd.DataFrame({
    "feature": feature_cols,
    "weight": model.coef_[0]
}).sort_values("weight", ascending=False)

print(coefficients)
