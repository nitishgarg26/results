# report_views.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def show_data_table(df):
    st.subheader("Filtered Data Table")
    st.dataframe(df)

def show_average_scores_chart(df):
    st.subheader("Average Scores by Student")

    avg_columns = [col for col in df.columns if col.endswith("AVG")]
    if not avg_columns:
        st.info("No AVG columns found for chart.")
        return

    plot_df = df[['STNAME'] + avg_columns].set_index('STNAME')
    st.bar_chart(plot_df)

def show_subject_heatmap(df):
    st.subheader("Student Subject Performance Heatmap")

    avg_columns = [col for col in df.columns if col.endswith("AVG")]
    if len(avg_columns) >= 2:
        pivot_df = df[['STNAME'] + avg_columns].set_index('STNAME')
        fig, ax = plt.subplots()
        sns.heatmap(pivot_df, annot=True, cmap="Blues", fmt=".1f", linewidths=.5, ax=ax)
        st.pyplot(fig)
    else:
        st.info("Not enough data to plot heatmap.")
