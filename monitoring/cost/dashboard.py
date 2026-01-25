import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://llmops:llmops@localhost:5432/llmops"

engine = create_engine(DATABASE_URL)

df_logs = pd.read_sql("SELECT * FROM inference_logs", engine)
df_feedback = pd.read_sql("SELECT * FROM feedback", engine)

st.title("LLMOps Cost vs Quality Dashboard")

if df_logs.empty or df_feedback.empty:
    st.warning("Not enough data yet.")
    st.stop()

merged = df_logs.merge(
    df_feedback,
    left_on=["prompt_name", "prompt_version"],
    right_on=["prompt_name", "prompt_version"],
    suffixes=("_log", "_fb")
)

st.subheader("Cost vs Quality")

st.scatter_chart(
    merged,
    x="cost",
    y="rating"
)

st.subheader("Latency vs Quality")

st.scatter_chart(
    merged,
    x="latency_ms",
    y="rating"
)

st.subheader("Summary Table")

st.dataframe(
    merged[[
        "prompt_name",
        "prompt_version",
        "cost",
        "latency_ms",
        "rating",
        "comment"
    ]]
)
