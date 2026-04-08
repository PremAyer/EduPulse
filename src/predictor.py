import joblib
import pandas as pd
import os

class PlacementPredictor:
    def __init__(self):
        model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')        
        self.classifier = joblib.load(os.path.join(model_dir, 'placement_classifier.pkl'))
        self.regressor = joblib.load(os.path.join(model_dir, 'salary_regressor.pkl'))
        self.features = ['coding_skill_score', 'aptitude_score', 'internships_count', 'projects_count', 'cgpa', 'backlogs']

    def predict(self, student_data):
            df = pd.DataFrame([student_data])[self.features]
            is_placed = self.classifier.predict(df)[0]
            
            if is_placed == 1:
                status = "Placed"
                salary = self.regressor.predict(df)[0]
            else:
                status = "Not Placed"
                salary = 0.00
                
            return status, round(salary, 2)
