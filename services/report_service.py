import pandas as pd
import numpy as np
from services.database_service import DatabaseService

class ReportService:
    def __init__(self):
        self.db_service = DatabaseService()
    
    def generate_student_report(self, student_id):
        """Generate comprehensive student report"""
        df = self.db_service.get_student_performance(student_id)
        
        if df.empty:
            return None
        
        # Calculate performance metrics
        report = {
            'student_info': {
                'name': df.iloc[0]['STNAME'],
                'father': df.iloc[0]['FATHER'],
                'roll_no': df.iloc[0]['ROLLNO'],
                'class': df.iloc[0]['CLASS']
            },
            'exam_count': len(df),
            'average_score': df['ExMk'].mean(),
            'best_score': df['ExMk'].max(),
            'worst_score': df['ExMk'].min(),
            'average_rank': df['ExRnk'].mean(),
            'best_rank': df['ExRnk'].min(),
            'subject_performance': {
                'Physics': {
                    'average': df['S1Mk'].mean(),
                    'max': df['S1Mk'].max(),
                    'min': df['S1Mk'].min()
                },
                'Chemistry': {
                    'average': df['S2Mk'].mean(),
                    'max': df['S2Mk'].max(),
                    'min': df['S2Mk'].min()
                },
                'Botany': {
                    'average': df['S3Mk'].mean(),
                    'max': df['S3Mk'].max(),
                    'min': df['S3Mk'].min()
                },
                'Zoology': {
                    'average': df['S4Mk'].mean(),
                    'max': df['S4Mk'].max(),
                    'min': df['S4Mk'].min()
                }
            },
            'exam_history': df
        }
        
        return report
    
    def generate_class_report(self, class_name, exam_id=None):
        """Generate class performance report"""
        df = self.db_service.get_class_analytics(class_name, exam_id)
        
        if df.empty:
            return None
        
        report = {
            'class_info': {
                'name': class_name,
                'total_students': len(df),
                'exam_name': df.iloc[0]['EXNM'] if exam_id else 'All Exams'
            },
            'score_statistics': {
                'average': df['ExMk'].mean(),
                'median': df['ExMk'].median(),
                'std_dev': df['ExMk'].std(),
                'max': df['ExMk'].max(),
                'min': df['ExMk'].min()
            },
            'subject_averages': {
                'Physics': df['S1Mk'].mean(),
                'Chemistry': df['S2Mk'].mean(),
                'Botany': df['S3Mk'].mean(),
                'Zoology': df['S4Mk'].mean()
            },
            'top_performers': df.nsmallest(10, 'ExRnk')[['STNAME', 'ExMk', 'ExRnk']],
            'data': df
        }
        
        return report
    
    def generate_comparative_analysis(self, exam_id):
        """Generate comparative analysis across classes"""
        df = self.db_service.get_exam_results(exam_id=exam_id)
        
        if df.empty:
            return None
        
        class_performance = df.groupby('CLASS').agg({
            'ExMk': ['mean', 'median', 'std', 'count'],
            'S1Mk': 'mean',
            'S2Mk': 'mean',
            'S3Mk': 'mean',
            'S4Mk': 'mean'
        }).round(2)
        
        return {
            'exam_name': df.iloc[0]['EXNM'],
            'total_students': len(df),
            'overall_average': df['ExMk'].mean(),
            'class_performance': class_performance,
            'data': df
        }
