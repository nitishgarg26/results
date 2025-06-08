import pandas as pd
import streamlit as st
from datetime import datetime
import re

def format_date(date_string):
    """Format date string for display"""
    try:
        if pd.isna(date_string):
            return "N/A"
        
        # Handle different date formats
        if isinstance(date_string, str):
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                try:
                    date_obj = datetime.strptime(date_string, fmt)
                    return date_obj.strftime('%d %b %Y')
                except ValueError:
                    continue
        
        return str(date_string)
    except:
        return "Invalid Date"

def format_score(score):
    """Format score for display"""
    try:
        if pd.isna(score):
            return "N/A"
        return f"{float(score):.1f}"
    except:
        return "N/A"

def format_rank(rank):
    """Format rank with ordinal suffix"""
    try:
        if pd.isna(rank):
            return "N/A"
        
        rank = int(rank)
        if 10 <= rank % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(rank % 10, 'th')
        
        return f"{rank}{suffix}"
    except:
        return "N/A"

def calculate_percentage(obtained, total):
    """Calculate percentage score"""
    try:
        if pd.isna(obtained) or pd.isna(total) or total == 0:
            return 0
        return (float(obtained) / float(total)) * 100
    except:
        return 0

def get_grade(percentage):
    """Get grade based on percentage"""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

def validate_student_id(student_id):
    """Validate student ID format"""
    if not student_id:
        return False
    
    # Basic validation - adjust pattern as needed
    pattern = r'^[A-Za-z0-9]+$'
    return bool(re.match(pattern, student_id))

def clean_phone_number(phone):
    """Clean and format phone number"""
    if pd.isna(phone):
        return "N/A"
    
    # Remove non-numeric characters
    phone_clean = re.sub(r'[^\d]', '', str(phone))
    
    # Format based on length
    if len(phone_clean) == 10:
        return f"{phone_clean[:3]}-{phone_clean[3:6]}-{phone_clean[6:]}"
    elif len(phone_clean) == 11 and phone_clean.startswith('1'):
        return f"+1-{phone_clean[1:4]}-{phone_clean[4:7]}-{phone_clean[7:]}"
    else:
        return phone_clean if phone_clean else "N/A"

def export_to_csv(dataframe, filename):
    """Export dataframe to CSV for download"""
    try:
        csv = dataframe.to_csv(index=False)
        return csv
    except Exception as e:
        st.error(f"Error exporting to CSV: {e}")
        return None

def filter_dataframe(df, filters):
    """Apply multiple filters to dataframe"""
    filtered_df = df.copy()
    
    for column, value in filters.items():
        if value and value != "All":
            if column in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[column] == value]
    
    return filtered_df

def get_performance_trend(scores):
    """Calculate performance trend (improving/declining/stable)"""
    if len(scores) < 2:
        return "Insufficient Data"
    
    # Calculate trend using linear regression slope
    x = list(range(len(scores)))
    y = scores
    
    n = len(scores)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(x[i] ** 2 for i in range(n))
    
    try:
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        if slope > 0.5:
            return "📈 Improving"
        elif slope < -0.5:
            return "📉 Declining"
        else:
            return "📊 Stable"
    except:
        return "Unable to Calculate"

def calculate_class_statistics(scores):
    """Calculate comprehensive class statistics"""
    if not scores or len(scores) == 0:
        return {}
    
    scores_series = pd.Series(scores)
    
    return {
        'mean': scores_series.mean(),
        'median': scores_series.median(),
        'mode': scores_series.mode().iloc[0] if not scores_series.mode().empty else scores_series.mean(),
        'std_dev': scores_series.std(),
        'variance': scores_series.var(),
        'min': scores_series.min(),
        'max': scores_series.max(),
        'range': scores_series.max() - scores_series.min(),
        'q1': scores_series.quantile(0.25),
        'q3': scores_series.quantile(0.75),
        'iqr': scores_series.quantile(0.75) - scores_series.quantile(0.25)
    }

def highlight_top_performers(df, score_column, top_n=5):
    """Highlight top performers in dataframe"""
    def highlight_top(row):
        if row.name < top_n:
            return ['background-color: #90EE90'] * len(row)
        else:
            return [''] * len(row)
    
    # Sort by score column in descending order
    df_sorted = df.sort_values(score_column, ascending=False)
    
    return df_sorted.style.apply(highlight_top, axis=1)

def generate_summary_stats(df, numeric_columns):
    """Generate summary statistics for numeric columns"""
    summary = {}
    
    for col in numeric_columns:
        if col in df.columns:
            summary[col] = {
                'count': df[col].count(),
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'median': df[col].median()
            }
    
    return summary
