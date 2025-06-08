import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from services.database_service import DatabaseService
from services.report_service import ReportService
from utils.visualizations import create_performance_chart, create_subject_radar_chart

def render_student_reports():
    """Render student reports page"""
    st.title("👤 Student Performance Reports")
    
    db_service = DatabaseService()
    report_service = ReportService()
    
    # Student selection
    students_df = db_service.get_all_students()
    
    if students_df.empty:
        st.warning("No student data available")
        return
    
    # Create student options
    student_options = [f"{row['STNAME']} ({row['STID']})" for _, row in students_df.iterrows()]
    selected_student = st.selectbox("Select Student", student_options)
    
    if selected_student:
        # Extract student ID
        student_id = selected_student.split("(")[-1].replace(")", "")
        
        # Generate report
        report = report_service.generate_student_report(student_id)
        
        if report:
            # Display student info
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Student Name", report['student_info']['name'])
            with col2:
                st.metric("Roll Number", report['student_info']['roll_no'])
            with col3:
                st.metric("Class", report['student_info']['class'])
            with col4:
                st.metric("Total Exams", report['exam_count'])
            
            # Performance metrics
            st.subheader("📊 Performance Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Average Score", f"{report['average_score']:.1f}")
            with col2:
                st.metric("Best Score", f"{report['best_score']}")
            with col3:
                st.metric("Average Rank", f"{report['average_rank']:.1f}")
            with col4:
                st.metric("Best Rank", f"{report['best_rank']}")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Score Trend")
                fig = create_performance_chart(report['exam_history'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🎯 Subject Performance")
                fig = create_subject_radar_chart(report['subject_performance'])
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed exam history
            st.subheader("📋 Exam History")
            display_columns = ['EXNM', 'ExDt', 'ExMk', 'ExRnk', 'S1Mk', 'S2Mk', 'S3Mk', 'S4Mk']
            st.dataframe(
                report['exam_history'][display_columns],
                column_config={
                    'EXNM': 'Exam Name',
                    'ExDt': 'Date',
                    'ExMk': 'Total Marks',
                    'ExRnk': 'Rank',
                    'S1Mk': 'Physics',
                    'S2Mk': 'Chemistry',
                    'S3Mk': 'Botany',
                    'S4Mk': 'Zoology'
                }
            )
