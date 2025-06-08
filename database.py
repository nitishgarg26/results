# database.py
import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_data(query, params=None):
    conn = get_connection()
    df = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows)
    finally:
        conn.close()
    return df
