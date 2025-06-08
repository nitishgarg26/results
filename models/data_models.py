from dataclasses import dataclass
from typing import Optional, List
import pandas as pd

@dataclass
class Student:
    stid: str
    stname: str
    father: str
    rollno: str
    class_name: str
    phone: Optional[str] = None

@dataclass
class ExamResult:
    stid: str
    exam_id: str
    exam_name: str
    exam_date: str
    total_marks: int
    rank: int
    class_rank: int
    physics_marks: int
    chemistry_marks: int
    botany_marks: int
    zoology_marks: int

@dataclass
class SubjectScore:
    subject_name: str
    max_marks: int
    obtained_marks: int
    correct_answers: int
    incorrect_answers: int
    unattempted: int
