import streamlit as st
from services.database_service import DatabaseService

def render_sidebar():
    """Render the sidebar with navigation and filters"""
    st.sidebar.title("📊 Exam Reports Dashboard")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Select Report Type",
        ["🏠 Home", "👤 Student Reports", "🎓 Class Reports", "📈 Analytics", "⚙️ Settings"]
    )
    
    # Database connection status
    db_service = DatabaseService()
    connection = db_service.db_config.get_connection()
    
    if connection:
        st.sidebar.success("✅ Database Connected")
        connection.close()
    else:
        st.sidebar.error("❌ Database Connection Failed")
    
    # Filters section
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters")
    
    # Get available data
    exams_df = db_service.get_available_exams()
    classes = db_service.get_available_classes()
    
    # Exam filter
    exam_options = ["All Exams"] + [f"{row['EXNM']} ({row['ExID']})" for _, row in exams_df.iterrows()]
    selected_exam = st.sidebar.selectbox("Select Exam", exam_options)
    
    # Class filter
    class_options = ["All Classes"] + classes
    selected_class = st.sidebar.selectbox("Select Class", class_options)
    
    # Extract exam ID
    exam_id = None
    if selected_exam != "All Exams":
        exam_id = selected_exam.split("(")[-1].replace(")", "")
    
    class_filter = None if selected_class == "All Classes" else selected_class
    
    return {
        'page': page,
        'exam_id': exam_id,
        'class_filter': class_filter,
        'selected_exam': selected_exam,
        'selected_class': selected_class
    }
