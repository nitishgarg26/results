import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_performance_chart(exam_history):
    """Create performance trend chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=exam_history['ExDt'],
        y=exam_history['ExMk'],
        mode='lines+markers',
        name='Total Marks',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Performance Trend Over Time",
        xaxis_title="Exam Date",
        yaxis_title="Marks",
        hovermode='x unified'
    )
    
    return fig

def create_subject_radar_chart(subject_performance):
    """Create radar chart for subject performance"""
    subjects = list(subject_performance.keys())
    averages = [subject_performance[subject]['average'] for subject in subjects]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=averages,
        theta=subjects,
        fill='toself',
        name='Average Performance'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(averages) * 1.1]
            )),
        showlegend=True,
        title="Subject-wise Performance"
    )
    
    return fig

def create_class_distribution_chart(data):
    """Create score distribution histogram"""
    fig = px.histogram(
        data, 
        x='ExMk', 
        nbins=20,
        title="Score Distribution",
        labels={'ExMk': 'Total Marks', 'count': 'Number of Students'}
    )
    
    fig.update_layout(
        xaxis_title="Total Marks",
        yaxis_title="Number of Students"
    )
    
    return fig

def create_subject_comparison_chart(subject_averages):
    """Create subject comparison bar chart"""
    subjects = list(subject_averages.keys())
    averages = list(subject_averages.values())
    
    fig = px.bar(
        x=subjects,
        y=averages,
        title="Subject-wise Class Average",
        labels={'x': 'Subjects', 'y': 'Average Marks'}
    )
    
    fig.update_layout(
        xaxis_title="Subjects",
        yaxis_title="Average Marks"
    )
    
    return fig
