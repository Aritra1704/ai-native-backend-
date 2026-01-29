import pandas as pd

data = [
    {"endpoint": "/pay", "latency_ms": 120, "status": 200},
    {"endpoint": "/pay", "latency_ms": 900, "status": 200},
    {"endpoint": "/pay", "latency_ms": 1500, "status": 500},
    {"endpoint": "/login", "latency_ms": 80, "status": 200},
    {"endpoint": "/login", "latency_ms": 300, "status": 200},
    {"endpoint": "/login", "latency_ms": 700, "status": 500},
]

df = pd.DataFrame(data)

df["is_error"] = df["status"] >= 500
df["is_slow"] = df["latency_ms"] > 800

signals = (
    df.groupby("endpoint")
      .agg(
          avg_latency=("latency_ms", "mean"),
          error_rate=("is_error", "mean"),
          slow_rate=("is_slow", "mean"),
          request_count=("status", "count")
      )
)

print(signals)

signals["high_risk"] = (
    (signals["error_rate"] > 0.3) |
    (signals["slow_rate"] > 0.4)
).astype(int)

print(signals)
