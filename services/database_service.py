import pandas as pd
import mysql.connector
from config.database import DatabaseConfig
import streamlit as st

class DatabaseService:
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_all_students(_self):
        """Fetch all students data"""
        connection = _self.db_config.get_connection()
        if not connection:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT DISTINCT STID, STNAME, FATHER, ROLLNO, CLASS, PHONE
            FROM exam_results
            ORDER BY STNAME
            """
            df = pd.read_sql(query, connection)
            return df
        except Exception as e:
            st.error(f"Error fetching students: {e}")
            return pd.DataFrame()
        finally:
            connection.close()
    
    @st.cache_data(ttl=300)
    def get_exam_results(_self, exam_id=None, class_filter=None):
        """Fetch exam results with optional filters"""
        connection = _self.db_config.get_connection()
        if not connection:
            return pd.DataFrame()
        
        try:
            query = "SELECT * FROM exam_results WHERE 1=1"
            params = []
            
            if exam_id:
                query += " AND ExID = %s"
                params.append(exam_id)
            
            if class_filter:
                query += " AND CLASS = %s"
                params.append(class_filter)
            
            query += " ORDER BY ExRnk"
            
            df = pd.read_sql(query, connection, params=params)
            return df
        except Exception as e:
            st.error(f"Error fetching exam results: {e}")
            return pd.DataFrame()
        finally:
            connection.close()
    
    @st.cache_data(ttl=300)
    def get_student_performance(_self, student_id):
        """Get performance data for a specific student"""
        connection = _self.db_config.get_connection()
        if not connection:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT * FROM exam_results 
            WHERE STID = %s 
            ORDER BY ExDt DESC
            """
            df = pd.read_sql(query, connection, params=[student_id])
            return df
        except Exception as e:
            st.error(f"Error fetching student performance: {e}")
            return pd.DataFrame()
        finally:
            connection.close()
    
    @st.cache_data(ttl=300)
    def get_class_analytics(_self, class_name, exam_id=None):
        """Get analytics for a specific class"""
        connection = _self.db_config.get_connection()
        if not connection:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT * FROM exam_results 
            WHERE CLASS = %s
            """
            params = [class_name]
            
            if exam_id:
                query += " AND ExID = %s"
                params.append(exam_id)
            
            query += " ORDER BY ExRnk"
            
            df = pd.read_sql(query, connection, params=params)
            return df
        except Exception as e:
            st.error(f"Error fetching class analytics: {e}")
            return pd.DataFrame()
        finally:
            connection.close()
    
    @st.cache_data(ttl=300)
    def get_available_exams(_self):
        """Get list of available exams"""
        connection = _self.db_config.get_connection()
        if not connection:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT DISTINCT ExID, EXNM, ExDt 
            FROM exam_results 
            ORDER BY ExDt DESC
            """
            df = pd.read_sql(query, connection)
            return df
        except Exception as e:
            st.error(f"Error fetching exams: {e}")
            return pd.DataFrame()
        finally:
            connection.close()
    
    @st.cache_data(ttl=300)
    def get_available_classes(_self):
        """Get list of available classes"""
        connection = _self.db_config.get_connection()
        if not connection:
            return []
        
        try:
            query = "SELECT DISTINCT CLASS FROM exam_results ORDER BY CLASS"
            df = pd.read_sql(query, connection)
            return df['CLASS'].tolist()
        except Exception as e:
            st.error(f"Error fetching classes: {e}")
            return []
        finally:
            connection.close()
