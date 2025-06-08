# data_utils.py
import pandas as pd

def filter_dataframe(df, class_name=None, exam_name=None):
    if class_name:
        df = df[df['CLASS'] == class_name]
    if exam_name:
        df = df[df['EXNM'] == exam_name]
    return df
