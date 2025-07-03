import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="GenBI Insurance Insights", layout="wide")
st.title("📊 GenBI - Insurance Business Insights")

# Initialize session state for history and responses
if "history" not in st.session_state:
    st.session_state.history = []

if "responses" not in st.session_state:
    st.session_state.responses = []

# User input
query = st.text_input("Ask a business question (e.g. 'Why did Q2 revenue drop in 2024?')", key="user_input")

# Submit button
if st.button("Submit"):
    if query.strip():
        st.session_state.history.append(query)

        # Call FastAPI backend
        with st.spinner("Analyzing with GenBI agents..."):
            response = requests.post("http://localhost:8000/process_query", json={
                "query": query,
                "history": st.session_state.history
            })

            if response.status_code == 200:
                result = response.json()
                summary = result.get("summary", "No summary returned.")
                data = result.get("data", [])

                st.session_state.responses.append(summary)

                # Display Executive Summary
                st.subheader("🧠 Executive Summary")
                st.markdown(f"**{summary}**")

                # Display Data
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
                st.error("❌ Error contacting FastAPI backend.")
    else:
        st.warning("Please enter a valid business question.")

# Display full chat history
if st.session_state.history:
    st.markdown("---")
    st.subheader("💬 Chat History")
    for user_msg, assistant_msg in zip(st.session_state.history, st.session_state.responses):
        st.markdown(f"**🧑 You:** {user_msg}")
        st.markdown(f"**🤖 GenBI:** {assistant_msg}")
