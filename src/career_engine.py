import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import os

class CareerRecommender:
    def __init__(self, data_path='data/Company Final Dataset.csv', model_path='models/career_model.pkl'):
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


    def train_model(self):
        """Trains the NLP model to predict Job Roles from Skills."""
        if self.df is None: return False
        
        # X = Features (Skills string), y = Target (Job Role)
        X = self.df['Skills Needed'].fillna('')
        y = self.df['Job Role']
        
        # Pipeline: Convert text to numbers (TF-IDF) -> Predict with Random Forest
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', RandomForestClassifier(n_estimators=200, random_state=42))
        ])
        
        self.model.fit(X, y)

        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        return True


    def predict_role(self, user_skills_str):
            """Predicts the best job role based on input skills."""
            # Auto-train or load if not in memory
            if self.model is None:
                if os.path.exists(self.model_path):
                    self.model = joblib.load(self.model_path)
                else:
                    self.train_model()

            predicted_role = self.model.predict([user_skills_str])[0]
            
            # Get confidence score
            probs = self.model.predict_proba([user_skills_str])[0]
            confidence = max(probs) * 100
            
            return predicted_role, round(confidence, 2)
    
    
    def analyze_company_fit(self, predicted_role, user_skills_input, top_n=6):
        """Scans ALL jobs in the database and returns the closest matches based on skills."""
        
        # 1. Clean the user's input into a set of lowercase skills
        user_skills_list = [s.strip().lower() for s in str(user_skills_input).split(',')]
        user_skills_set = set(user_skills_list)
        
        results = []

        # 2. Iterate through EVERY row in your dataset
        for index, row in self.df.iterrows():
            company = row['Company']
            role = row['Job Role']
            
            # Clean the required skills from the database
            req_skills_str = str(row['Skills Needed']).lower()
            req_skills_set = set([s.strip() for s in req_skills_str.split(',') if s.strip()])
            
            if not req_skills_set:
                continue
                
            # 3. Calculate how many skills match
            overlap = user_skills_set.intersection(req_skills_set)
            match_percentage = (len(overlap) / len(req_skills_set)) * 100
            
            # 4. Figure out exactly what they are missing
            missing_skills = req_skills_set - user_skills_set
            missing_skills_str = ", ".join([s.title() for s in missing_skills])
            
            if not missing_skills_str:
                missing_skills_str = "None - Fully Aligned!"
                
            # Add to our list
            results.append({
                "Company": company,
                "Suggested Role": role, # We show the actual role from the DB now
                "Match Quotient": match_percentage,
                "Deficit Analysis (Required Upskilling)": missing_skills_str
            })
            
        # 5. Turn into a Dataframe, sort by best match, and grab the top N results
        final_df = pd.DataFrame(results)
        
        if not final_df.empty:
            final_df = final_df.sort_values(by="Match Quotient", ascending=False).head(top_n)
            
        return final_df



        

