import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("LLMOps Feedback Console")

prompt_name = st.text_input("Prompt Name", value="qa")
prompt_version = st.number_input("Prompt Version", min_value=1, value=1)
user_input = st.text_area("User Input")
model_output = st.text_area("Model Output")

rating = st.slider("Rating (1 = bad, 5 = good)", 1, 5, 3)
comment = st.text_area("Comment (optional)")

if st.button("Submit Feedback"):
    payload = {
        "prompt_name": prompt_name,
        "prompt_version": prompt_version,
        "user_input": user_input,
        "model_output": model_output,
        "rating": rating,
        "comment": comment
    }

    resp = requests.post(f"{API_URL}/feedback", json=payload)

    if resp.status_code == 200:
        st.success("Feedback submitted!")
    else:
        st.error("Failed to submit feedback")
