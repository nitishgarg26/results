import streamlit as st
from components.sidebar import render_sidebar
from components.student_reports import render_student_reports
from components.class_reports import render_class_reports
from components.analytics import render_analytics
import os

# Page configuration
st.set_page_config(
    page_title="Exam Reports Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Render sidebar and get navigation state
    sidebar_state = render_sidebar()
    
    # Route to appropriate page
    if sidebar_state['page'] == "🏠 Home":
        render_home()
    elif sidebar_state['page'] == "👤 Student Reports":
        render_student_reports()
    elif sidebar_state['page'] == "🎓 Class Reports":
        render_class_reports()
    elif sidebar_state['page'] == "📈 Analytics":
        render_analytics()
    elif sidebar_state['page'] == "⚙️ Settings":
        render_settings()

def render_home():
    """Render home page"""
    st.markdown('<h1 class="main-header">📊 Exam Reports Dashboard</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to the Exam Reports Dashboard
    
    This application provides comprehensive reporting and analytics for exam results data.
    
    ### Features:
    - **👤 Student Reports**: Individual student performance analysis
    - **🎓 Class Reports**: Class-wise performance statistics
    - **📈 Analytics**: Advanced analytics and comparisons
    - **⚙️ Settings**: Database configuration and settings
    
    ### Quick Start:
    1. Use the sidebar to navigate between different report types
    2. Apply filters to focus on specific exams or classes
    3. Export reports for further analysis
    
    ### Database Status:
    """)
    
    # Add database status check here
    from services.database_service import DatabaseService
    db_service = DatabaseService()
    connection = db_service.db_config.get_connection()
    
    if connection:
        st.success("✅ Database connection is active")
        
        # Show quick stats
        students_df = db_service.get_all_students()
        exams_df = db_service.get_available_exams()
        classes = db_service.get_available_classes()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Students", len(students_df))
        with col2:
            st.metric("Total Exams", len(exams_df))
        with col3:
            st.metric("Total Classes", len(classes))
        
        connection.close()
    else:
        st.error("❌ Database connection failed. Please check your configuration.")

def render_settings():
    """Render settings page"""
    st.title("⚙️ Settings")
    
    st.subheader("Database Configuration")
    
    # Environment variables info
    st.info("""
    Configure your database connection using environment variables:
    - `DB_HOST`: Database host
    - `DB_NAME`: Database name
    - `DB_USER`: Database username
    - `DB_PASSWORD`: Database password
    - `DB_PORT`: Database port (default: 3306)
    """)
    
    # Show current configuration (without sensitive data)
    from config.database import DatabaseConfig
    config = DatabaseConfig()
    
    st.write("**Current Configuration:**")
    st.write(f"- Host: {config.host}")
    st.write(f"- Database: {config.database}")
    st.write(f"- User: {config.user}")
    st.write(f"- Port: {config.port}")

if __name__ == "__main__":
    main()
