import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import os

class CareerRecommender:
    def __init__(self, data_path='data/Dataset_company_job roles.csv', model_path='models/career_model.pkl'):
        self.data_path = data_path
        self.model_path = model_path
        self.model = None
        self.df = None
        self._load_data()

    def _load_data(self):
        """Loads the dataset and standardizes column names."""
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
            self.df.columns = [c.strip() for c in self.df.columns]
        else:
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
