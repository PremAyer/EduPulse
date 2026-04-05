import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import os


print("Loading dataset...")
df = pd.read_csv('Student Dataset.csv')

# 1. Separate Features and Target
X = df.drop(columns=['Student id', 'Academic status'], errors='ignore')
y = df['Academic status']


# We use learning_rate and max_depth to control how it learns
model = GradientBoostingClassifier(
    n_estimators=100, 
    learning_rate=0.1,  # How much each tree contributes to the final result
    max_depth=5,        # Keeps the individual trees relatively shallow to prevent overfitting
    random_state=42
)

model.fit(X, y)