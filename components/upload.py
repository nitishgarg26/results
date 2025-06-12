# pages/upload.py

import streamlit as st
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306)),
    )

def render():
    st.title("Upload Exam Results CSV to MySQL")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview:", df.head())

        if st.button("Append/Update to Database"):
            columns = list(df.columns)
            col_str = ", ".join(f"`{c}`" for c in columns)
            val_str = ", ".join(["%s"] * len(columns))
            update_str = ", ".join(
                f"`{c}`=VALUES(`{c}`)" for c in columns if c not in ["STID", "ExID"]
            )

            query = f"""
                INSERT INTO exam_results ({col_str})
                VALUES ({val_str})
                ON DUPLICATE KEY UPDATE {update_str}
            """

            conn = None
            cursor = None
            try:
                conn = get_connection()
                if conn is None:
                    raise ConnectionError("Unable to establish database connection")
                cursor = conn.cursor()
                data = [tuple(row) for row in df.values]
                cursor.executemany(query, data)
                conn.commit()
                st.success(
                    f"Uploaded {cursor.rowcount} rows to the database."
                )
            except Exception as e:
                st.error(f"Database error: {e}")
            finally:
                if cursor is not None:
                    cursor.close()
                if conn is not None:
                    conn.close()
