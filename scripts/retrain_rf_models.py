"""
Retrain ALL Models - Fix for Inverted Predictions
This script retrains Random Forest AND Logistic Regression models with correct labels
All models will use the same 6-feature format with BMI
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import joblib
import os

print("="*60)
print("RETRAINING ALL MODELS (RF + LR)")
print("="*60)

# 1. Load the dataset
print("\n1. Loading dataset...")
df = pd.read_csv('cardio_train_properly_separated_comma.csv')
print(f"✓ Dataset loaded: {df.shape}")
print(f"  Columns: {list(df.columns)}")

# 2. Check the target variable
print("\n2. Checking target variable (cardio)...")
print(f"  Value counts:\n{df['cardio'].value_counts()}")
print(f"  0 = No Disease, 1 = Disease Present")

# 3. Feature engineering (same as in Project_Organized.ipynb)
print("\n3. Feature engineering...")
# Convert age from days to years
df['age_years'] = df['age'] / 365
# Calculate BMI
df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
print(f"✓ Created age_years and bmi features")

# 4. Select features (same as Logistic Regression)
print("\n4. Selecting features...")
feature_cols = ['ap_hi', 'ap_lo', 'age_years', 'cholesterol', 'bmi', 'weight']
X = df[feature_cols]
y = df['cardio']
print(f"✓ Features selected: {feature_cols}")
print(f"  X shape: {X.shape}")
print(f"  y shape: {y.shape}")
print(f"  Target distribution: {y.value_counts().to_dict()}")

# 5. Train-test split
print("\n5. Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✓ Train set: {X_train.shape}, Test set: {X_test.shape}")
