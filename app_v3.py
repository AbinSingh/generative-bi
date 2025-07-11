import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(page_title="GenBI Insurance Insights", layout="wide")
st.title("💬 GenBI - Business Chat Assistant")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "responses" not in st.session_state:
    st.session_state.responses = []

# Display chat history
st.markdown("---")
st.subheader("📚 Conversation")

for i in range(len(st.session_state.history)):
    user_msg = st.session_state.history[i]
    assistant_msg = st.session_state.responses[i]

    st.markdown(
        f"<div style='background-color:#e0f7fa; padding:10px; border-radius:10px; margin-bottom:5px'>"
        f"<b>🧑 You:</b><br>{user_msg}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='background-color:#f1f8e9; padding:10px; border-radius:10px; margin-bottom:20px'>"
        f"<b>🤖 GenBI:</b><br>{assistant_msg}</div>",
        unsafe_allow_html=True,
    )

# Input and send button at bottom
st.markdown("---")
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input("Type your message", key="user_input", label_visibility="collapsed")
with col2:
    send = st.button("Send")

# On send
if send:
    if query.strip():
        st.session_state.history.append(query)

        with st.spinner("Thinking..."):
            response = requests.post("http://localhost:8000/process_query", json={
                "query": query,
                "history": st.session_state.history
            })

            if response.status_code == 200:
                result = response.json()
                summary = result.get("summary", "No summary returned.")
                data = result.get("data", [])

                st.session_state.responses.append(summary)

                # Immediately show response
                st.markdown(
                    f"<div style='background-color:#f1f8e9; padding:10px; border-radius:10px; margin-bottom:20px'>"
                    f"<b>🤖 GenBI:</b><br>{summary}</div>",
                    unsafe_allow_html=True,
                )

                # Optional data visualization
                if data:
                    df = pd.DataFrame(data)
                    st.subheader("📈 Data Insights")

                    if "issue_date" in df.columns and df.select_dtypes(include='number').shape[1] >= 1:
                        metric = df.select_dtypes(include='number').columns[0]
                        fig = px.line(df, x="issue_date", y=metric, title=f"{metric} Over Time")
                        st.plotly_chart(fig)
                    else:
                        st.dataframe(df)
                else:
                    st.info("No data returned from backend.")
            else:
                st.session_state.responses.append("❌ Error contacting FastAPI backend.")
                st.error("❌ Error contacting FastAPI backend.")
    else:
        st.warning("Please enter a valid business question.")

st.rerun()
