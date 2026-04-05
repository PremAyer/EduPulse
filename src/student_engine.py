import pandas as pd
import joblib

class StudentPredictor:
    def __init__(self):
        try:
            self.model = joblib.load('models/student_performance_model.pkl')

            self.features = [
                'previous_semester_sgpa', 
                'Attendance marks', 
                'assignment_score_average(out of 20)',
                'midterm_exam_avg', 
                'Lowest midterm_exam_score'
            ]

        except FileNotFoundError:
            self.model = None
        
    def predict_performance(self, df):
            if self.model is None:
                return None, "Model not found. Please run train_student_model.py first."
