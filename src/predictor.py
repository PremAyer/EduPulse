import joblib
import pandas as pd
import os

class PlacementPredictor:
    def __init__(self):
        # Load the models when the class is instantiated
        model_dir = os.path.join(os.path.dirname(__file__), 'models')
        self.classifier = joblib.load(os.path.join(model_dir, 'placement_classifier.pkl'))
        self.regressor = joblib.load(os.path.join(model_dir, 'salary_regressor.pkl'))
        self.features = ['coding_score', 'aptitude_score', 'internships_count', 'projects_count', 'cgpa', 'backlogs']

