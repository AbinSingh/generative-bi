
# 4. Streamlit Frontend (app.py)
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GenBI Insurance Insights", layout="wide")
st.title("📊 GenBI - Insurance Business Insights")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a business question (e.g. 'Why did Q2 revenue drop in 2024?')")

if st.button("Submit"):
    if query:
        st.session_state.history.append(query)
        with st.spinner("Analyzing..."):
            response = requests.post("http://localhost:8000/process_query", json={
                "query": query,
                "history": st.session_state.history
            })
            result = response.json()
            st.subheader("Executive Summary")
            st.write(result["summary"])

            if result["data"]:
                df = pd.DataFrame(result["data"])
                st.subheader("📈 Data Visualization")
                if "issue_date" in df.columns and df.select_dtypes(include='number').shape[1] >= 1:
                    metric = df.select_dtypes(include='number').columns[0]
                    fig = px.line(df, x="issue_date", y=metric, title=f"{metric} Over Time")
                    st.plotly_chart(fig)
                else:
                    st.dataframe(df)
    else:
        st.warning("Please enter a question.")
