# app.py
import streamlit as st
import pandas as pd
from database import fetch_data
from data_utils import filter_dataframe
from report_views import show_data_table, show_average_scores_chart, show_subject_heatmap

st.set_page_config(page_title="Student Reports", layout="wide")
st.title("📊 Student Report Dashboard")

# Fetch all data once (you can cache this if data is huge)
query = "SELECT * FROM your_table"
df = fetch_data(query)

# Sidebar Filters
st.sidebar.header("Filter Options")
classes = sorted(df['CLASS'].dropna().unique())
exams = sorted(df['EXNM'].dropna().unique())

selected_class = st.sidebar.selectbox("Select Class", [""] + list(classes))
selected_exam = st.sidebar.selectbox("Select Exam", [""] + list(exams))

# Filter data
filtered_df = filter_dataframe(df, selected_class, selected_exam)

# Display views
show_data_table(filtered_df)
show_average_scores_chart(filtered_df)
show_subject_heatmap(filtered_df)
