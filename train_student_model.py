import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import os


print("Loading dataset...")
df = pd.read_csv('Student Dataset.csv')

# 1. Separate Features and Target
X = df.drop(columns=['Student id', 'Academic status'], errors='ignore')
y = df['Academic status']