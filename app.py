import streamlit as st
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Page configuration
st.set_page_config(
    page_title="Exam Reports Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import components with error handling
try:
    from components.sidebar import render_sidebar
    from components.student_reports import render_student_reports
    from components.class_reports import render_class_reports
    from components.analytics import render_analytics
    from components.upload import render
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Please ensure all required files are present in the repository.")
    st.stop()

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
    try:
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
        elif sidebar_state['page'] == "Upload Results":
            render()
        elif sidebar_state['page'] == "⚙️ Settings":
            render_settings()
    except Exception as e:
        st.error(f"Application Error: {e}")
        st.error("Please check your database configuration and ensure all files are properly set up.")

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
    """)

def render_settings():
    """Render settings page"""
    st.title("⚙️ Settings")
    
    st.subheader("Database Configuration")
    
    st.info("""
    Configure your database connection using Streamlit secrets:
    - Go to your app settings on Streamlit Cloud
    - Add your database credentials in the secrets section
    """)

if __name__ == "__main__":
    main()
