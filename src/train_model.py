import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib
import os

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

def train_and_save_models(data_path):
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Assuming these are your core columns based on your dummy code
    features = ['coding_skill_score', 'aptitude_score', 'internships_count', 'projects_count', 'cgpa', 'backlogs']
    
    X = df[features]
    
    # 1. Train Classification Model (Placed vs Not Placed)
    # Convert 'Placed'/'Not Placed' to 1/0
    y = df['placement_status'].apply(lambda x: 1 if x.strip().lower() == 'placed' else 0)

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y, test_size=0.2, random_state=42)
    
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train_c, y_train_c)

    preds_c = classifier.predict(X_test_c)
    print(f"Classification Accuracy: {accuracy_score(y_test_c, preds_c) * 100:.2f}%")
    
    joblib.dump(classifier, 'models/placement_classifier.pkl')
    print("Saved placement classifier.")


    # 2. Train Regression Model (Salary Prediction - only on PLACED students)
    placed_df = df[df['placement_status'].str.strip().str.lower() == 'placed']
    X_reg = placed_df[features]
    y_reg = placed_df['salary_package_lpa']
    



    