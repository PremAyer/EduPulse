import joblib
import pandas as pd
import os

class PlacementPredictor:
    def __init__(self):
        # Load the models when the class is instantiated
        model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')        
        self.classifier = joblib.load(os.path.join(model_dir, 'placement_classifier.pkl'))
        self.regressor = joblib.load(os.path.join(model_dir, 'salary_regressor.pkl'))
        self.features = ['coding_skill_score', 'aptitude_score', 'internships_count', 'projects_count', 'cgpa', 'backlogs']

    def predict(self, student_data):
            # Convert dictionary to DataFrame for prediction
            df = pd.DataFrame([student_data])[self.features]
            
            # Predict Status
            is_placed = self.classifier.predict(df)[0]
            
            if is_placed == 1:
                status = "Placed"
                salary = self.regressor.predict(df)[0]
            else:
                status = "Not Placed"
                salary = 0.00
                
            return status, round(salary, 2)

# # Step 1: Create an instance of the class (Build the car)
# my_predictor = PlacementPredictor()
