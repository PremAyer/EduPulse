import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import os


print("Loading dataset...")
df = pd.read_csv('data/Student Dataset.csv')
X = df.drop(columns=['Student id', 'Academic status'], errors='ignore')
y = df['Academic status']

model = GradientBoostingClassifier(
    n_estimators=100, 
    learning_rate=0.1,  
    max_depth=5,        
    random_state=42
)
model.fit(X, y)

os.makedirs('models', exist_ok=True)
model_path = 'models/student_performance_model.pkl'
joblib.dump(model, model_path)

print(f"✅ Success! Gradient Boosting Model trained and saved to {model_path}")