import streamlit as st
import plotly.express as px
from services.database_service import DatabaseService
from services.report_service import ReportService
from utils.visualizations import create_class_distribution_chart, create_subject_comparison_chart

def render_class_reports():
    """Render class reports page"""
    st.title("🎓 Class Performance Reports")
    
    db_service = DatabaseService()
    report_service = ReportService()
    
    # Get available classes and exams
    classes = db_service.get_available_classes()
    exams_df = db_service.get_available_exams()
    
    if not classes:
        st.warning("No class data available")
        return
    
    # Class and exam selection
    col1, col2 = st.columns(2)
    
    with col1:
        selected_class = st.selectbox("Select Class", classes, key="class_report_class_select")
    
    with col2:
        exam_options = ["All Exams"] + [f"{row['EXNM']} ({row['ExID']})" for _, row in exams_df.iterrows()]
        selected_exam = st.selectbox("Select Exam", exam_options, key="class_report_exam_select")
    
    # Extract exam ID
    exam_id = None
    if selected_exam != "All Exams":
        exam_id = selected_exam.split("(")[-1].replace(")", "")
    
    # Generate report
    report = report_service.generate_class_report(selected_class, exam_id)
    
    if report:
        # Class overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", report['class_info']['total_students'])
        with col2:
            st.metric("Class Average", f"{report['score_statistics']['average']:.1f}")
        with col3:
            st.metric("Highest Score", f"{report['score_statistics']['max']}")
        with col4:
            st.metric("Lowest Score", f"{report['score_statistics']['min']}")
        
        # Statistics
        st.subheader("📊 Score Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Median Score", f"{report['score_statistics']['median']:.1f}")
        with col2:
            st.metric("Standard Deviation", f"{report['score_statistics']['std_dev']:.1f}")
        with col3:
            pass  # Reserved for future metrics
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Score Distribution")
            fig = create_class_distribution_chart(report['data'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Subject Averages")
            fig = create_subject_comparison_chart(report['subject_averages'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Top performers
        st.subheader("🏆 Top Performers")
        st.dataframe(
            report['top_performers'],
            column_config={
                'STNAME': 'Student Name',
                'ExMk': 'Total Marks',
                'ExRnk': 'Rank'
            }
        )
        
        # Detailed results
        with st.expander("📋 Detailed Results"):
            display_columns = ['STNAME', 'ROLLNO', 'ExMk', 'ExRnk', 'S1Mk', 'S2Mk', 'S3Mk', 'S4Mk']
            st.dataframe(
                report['data'][display_columns],
                column_config={
                    'STNAME': 'Student Name',
                    'ROLLNO': 'Roll Number',
                    'ExMk': 'Total Marks',
                    'ExRnk': 'Rank',
                    'S1Mk': 'Physics',
                    'S2Mk': 'Chemistry',
                    'S3Mk': 'Botany',
                    'S4Mk': 'Zoology'
                }
            )
