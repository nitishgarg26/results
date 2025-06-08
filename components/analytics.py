import streamlit as st
import plotly.express as px
from services.database_service import DatabaseService
from services.report_service import ReportService

def render_analytics():
    """Render analytics page"""
    st.title("📈 Advanced Analytics")
    
    db_service = DatabaseService()
    report_service = ReportService()
    
    # Get available data
    exams_df = db_service.get_available_exams()
    
    if exams_df.empty:
        st.warning("No exam data available for analytics")
        return
    
    st.subheader("📊 Exam Comparison")
    
    # Exam selection for comparison
    exam_options = [f"{row['EXNM']} ({row['ExID']})" for _, row in exams_df.iterrows()]
    selected_exam = st.selectbox("Select Exam for Analysis", exam_options)
    
    if selected_exam:
        exam_id = selected_exam.split("(")[-1].replace(")", "")
        
        # Generate comparative analysis
        analysis = report_service.generate_comparative_analysis(exam_id)
        
        if analysis:
            # Display overall statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Students", analysis['total_students'])
            with col2:
                st.metric("Overall Average", f"{analysis['overall_average']:.1f}")
            with col3:
                st.metric("Exam", analysis['exam_name'])
            
            # Class performance comparison
            st.subheader("🏫 Class Performance Comparison")
            
            if not analysis['class_performance'].empty:
                # Create comparison chart
                class_data = analysis['class_performance'].reset_index()
                
                fig = px.bar(
                    x=class_data.index,
                    y=class_data[('ExMk', 'mean')],
                    title="Average Scores by Class",
                    labels={'x': 'Class', 'y': 'Average Score'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display detailed table
                st.dataframe(analysis['class_performance'])
            else:
                st.info("No class performance data available")
        else:
            st.error("Unable to generate analysis for selected exam")
