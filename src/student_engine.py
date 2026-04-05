import pandas as pd
import joblib

class StudentPredictor:
    def __init__(self):
        try:
            self.model = joblib.load('models/student_performance_model.pkl')
            