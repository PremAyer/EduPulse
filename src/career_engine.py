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
    
    
    def analyze_company_fit(self, predicted_role, user_skills_str):
        """Finds companies for the role and calculates exact missing skills."""
        # Filter dataset for the predicted role
        role_df = self.df[self.df['Job Role'] == predicted_role]
        
        # Removes all spaces and capitals from the user's input
        user_skills_set = set([s.strip().lower().replace(" ", "") for s in user_skills_str.split(',')])      
        
        company_results = []

        
        for _, row in role_df.iterrows():
            company = row['Company']
            req_skills_str = str(row['Skills Needed'])
            
            # 1. Keep original capitalization for the UI
            raw_req_skills = [s.strip().lower() for s in req_skills_str.split(',')]
            
            matched_count = 0
            missing_skills = []
            
            # 2. Check using lowercase, but save the original word
            for req_skill in raw_req_skills:
                # Removes spaces and capitals from the Excel data just for the check
                if req_skill.lower().replace(" ", "") in user_skills_set:
                    matched_count += 1
                else:
                    missing_skills.append(req_skill)
            
            # 3. Calculate match percentage
            score = (matched_count / len(raw_req_skills)) * 100 if raw_req_skills else 0
            
            company_results.append({
                'Company': company,
                'Match Score': score,
                'Formatted Score': f"{score:.0f}%",
                'Required Skills': req_skills_str,
                # 4. Remove .title() so it doesn't mess up things like "MySQL" or "AI"
                'Skills to Learn': ", ".join(missing_skills) if missing_skills else "None! You are ready."
            })
            
        # Sort by best match score descending
        company_results.sort(key=lambda x: x['Match Score'], reverse=True)
        
        # Return as a DataFrame for Streamlit
        return pd.DataFrame(company_results).drop(columns=['Match Score'])

  



        

