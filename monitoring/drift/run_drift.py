import pandas as pd
from sqlalchemy import create_engine
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

DATABASE_URL = "postgresql://llmops:llmops@localhost:5432/llmops"

engine = create_engine(DATABASE_URL)

def load_logs(limit: int = 200):
    query = f"""
        SELECT
            prompt_version,
            latency_ms,
            token_count,
            created_at
        FROM inference_logs
        ORDER BY created_at ASC
        LIMIT {limit}
    """
    return pd.read_sql(query, engine)

def run_drift_detection():
    df = load_logs()

    if len(df) < 20:
        print("Not enough data for drift detection")
        return

    midpoint = len(df) // 2
    reference = df.iloc[:midpoint]
    current = df.iloc[midpoint:]

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)

    report.save_html("monitoring/drift/drift_report.html")
    print("Drift report generated at monitoring/drift/drift_report.html")

if __name__ == "__main__":
    run_drift_detection()
