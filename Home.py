import streamlit as st
import pandas as pd
from app.data.incidents import get_all_incidents

st.title("First page")
st.subheader("This is the subheader")

username = st.text_input("Enter username")
if st.button("Login"):
    st.success(f"Hello {username} ")

df = pd.DataFrame({
    "User": ["Alice", "Bob", "Charlie"],
    "Score": [52,60,88]
})

st.dataframe(df)

st.subheader("Cyber Incidents")
df_incidents = get_all_incidents()

# metrix
col1, col2 = st.columns(2)

with col1:
    st.metric("High", df_incidents[df_incidents["severity"] == "High"].shape[0])

with col2:
    st.metric("Incidents", df_incidents["severity"].count(), "1")


# Barchart
severity_counts = df_incidents["severity"].value_counts().reset_index()
severity_counts.columns = ["severity", "count"]

st.bar_chart(severity_counts.set_index("severity"))