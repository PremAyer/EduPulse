import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib
import os

os.makedirs('models', exist_ok=True)

def train_and_save_models(data_path):
    print("Loading data...")
    df = pd.read_csv(data_path)
    features = ['coding_skill_score', 'aptitude_score', 'internships_count', 'projects_count', 'cgpa', 'backlogs']
    
    X = df[features]
    y = df['placement_status'].apply(lambda x: 1 if x.strip().lower() == 'placed' else 0)

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y, test_size=0.2, random_state=42)
    
    classifier = RandomForestClassifier(n_estimators=400,        
    max_depth=10,              
    min_samples_split=5,       
    class_weight='balanced', 
    random_state=42,
    n_jobs=-1
)
    classifier.fit(X_train_c, y_train_c)

    preds_c = classifier.predict(X_test_c)
    print(f"Classification Accuracy: {accuracy_score(y_test_c, preds_c) * 100:.2f}%")
    
    joblib.dump(classifier, 'models/placement_classifier.pkl')
    print("Saved placement classifier.")


    # Train Regression Model
    placed_df = df[df['placement_status'].str.strip().str.lower() == 'placed']
    X_reg = placed_df[features]
    y_reg = placed_df['salary_package_lpa']

    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    
    regressor = RandomForestRegressor(n_estimators=400,          
    max_depth=10,                 
    random_state=42,
    n_jobs=-1
)
    regressor.fit(X_train_r, y_train_r)

    preds_r = regressor.predict(X_test_r)
    print(f"Regression RMSE: {mean_squared_error(y_test_r, preds_r) ** 0.5:.2f} LPA")
    
    joblib.dump(regressor, 'models/salary_regressor.pkl')
    print("Saved salary regressor.")

if __name__ == "__main__":
    train_and_save_models('data/cleaned_placement_data.csv')

    
    

    



    