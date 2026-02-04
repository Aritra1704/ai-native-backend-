
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from week1_signal_design.signal_design import build_signals

signals = build_signals()


# Normalize latency
signals["latency_norm"] = signals["avg_latency"] / signals["avg_latency"].max()

# Combine failure signals
signals["instability_score"] = (
    0.6 * signals["error_rate"] +
    0.4 * signals["slow_rate"]
)

# Volume-adjusted risk
signals["risk_weighted"] = (
    signals["instability_score"] *
    signals["request_count"]
)

print(signals)

