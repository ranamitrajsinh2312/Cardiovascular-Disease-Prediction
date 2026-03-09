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
print(f"  Train target distribution: {y_train.value_counts().to_dict()}")
print(f"  Test target distribution: {y_test.value_counts().to_dict()}")

# 6. Create preprocessor (same as before)
print("\n6. Creating preprocessor...")

# Identify numeric and categorical columns
numeric_features = ['ap_hi', 'ap_lo', 'age_years', 'bmi', 'weight']
categorical_features = ['cholesterol']

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
    ]
)

# Fit preprocessor
preprocessor.fit(X_train)
print(f"✓ Preprocessor created and fitted")

# Transform data
X_train_processed = preprocessor.transform(X_train)
X_test_processed = preprocessor.transform(X_test)
print(f"  Processed train shape: {X_train_processed.shape}")
print(f"  Processed test shape: {X_test_processed.shape}")

# 7. Train Baseline Random Forest
print("\n7. Training Baseline Random Forest...")
baseline_rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
baseline_rf.fit(X_train_processed, y_train)
print(f"✓ Baseline RF trained")

# Evaluate baseline
y_pred_baseline = baseline_rf.predict(X_test_processed)
y_proba_baseline = baseline_rf.predict_proba(X_test_processed)

print("\n  Baseline RF Metrics:")
print(f"    Accuracy:  {accuracy_score(y_test, y_pred_baseline):.4f}")
print(f"    Precision: {precision_score(y_test, y_pred_baseline):.4f}")
print(f"    Recall:    {recall_score(y_test, y_pred_baseline):.4f}")
print(f"    F1 Score:  {f1_score(y_test, y_pred_baseline):.4f}")
print(f"    ROC AUC:   {roc_auc_score(y_test, y_proba_baseline[:, 1]):.4f}")

# 8. Train Tuned Random Forest
print("\n8. Training Tuned Random Forest (GridSearchCV)...")
print("  This may take a few minutes...")

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42, n_jobs=-1),
    param_grid,
    cv=3,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train_processed, y_train)
tuned_rf = grid_search.best_estimator_

print(f"✓ Tuned RF trained")
print(f"  Best parameters: {grid_search.best_params_}")

# Evaluate tuned
y_pred_tuned = tuned_rf.predict(X_test_processed)
y_proba_tuned = tuned_rf.predict_proba(X_test_processed)

print("\n  Tuned RF Metrics:")
print(f"    Accuracy:  {accuracy_score(y_test, y_pred_tuned):.4f}")
print(f"    Precision: {precision_score(y_test, y_pred_tuned):.4f}")
print(f"    Recall:    {recall_score(y_test, y_pred_tuned):.4f}")
print(f"    F1 Score:  {f1_score(y_test, y_pred_tuned):.4f}")
print(f"    ROC AUC:   {roc_auc_score(y_test, y_proba_tuned[:, 1]):.4f}")

# 9. Verify predictions with test cases
print("\n9. Verifying predictions with test cases...")

# High risk patient
high_risk_data = pd.DataFrame({
    'ap_hi': [180],
    'ap_lo': [80],
    'age_years': [70],
    'cholesterol': [3],
    'bmi': [39.8],
    'weight': [115.0]
})

# Low risk patient
low_risk_data = pd.DataFrame({
    'ap_hi': [110],
    'ap_lo': [70],
    'age_years': [30],
    'cholesterol': [1],
    'bmi': [22.5],
    'weight': [65.0]
})

# Process and predict
high_risk_processed = preprocessor.transform(high_risk_data)
low_risk_processed = preprocessor.transform(low_risk_data)

print("\n  HIGH RISK Patient (Age 70, Obese, Hypertension, High Chol):")
print(f"    Baseline RF: {baseline_rf.predict_proba(high_risk_processed)[0]}")
print(f"    Tuned RF:    {tuned_rf.predict_proba(high_risk_processed)[0]}")
print(f"    Expected: [low_prob, HIGH_prob] where HIGH_prob > 0.5")

print("\n  LOW RISK Patient (Age 30, Normal weight, Normal BP, Normal Chol):")
print(f"    Baseline RF: {baseline_rf.predict_proba(low_risk_processed)[0]}")
print(f"    Tuned RF:    {tuned_rf.predict_proba(low_risk_processed)[0]}")
print(f"    Expected: [HIGH_prob, low_prob] where HIGH_prob > 0.5")

# 10. Train Logistic Regression
print("\n10. Training Logistic Regression...")
from sklearn.linear_model import LogisticRegression

lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_processed, y_train)
print(f"✓ Logistic Regression trained")

# Evaluate LR
y_pred_lr = lr_model.predict(X_test_processed)
y_proba_lr = lr_model.predict_proba(X_test_processed)

print("\n  Logistic Regression Metrics:")
print(f"    Accuracy:  {accuracy_score(y_test, y_pred_lr):.4f}")
print(f"    Precision: {precision_score(y_test, y_pred_lr):.4f}")
print(f"    Recall:    {recall_score(y_test, y_pred_lr):.4f}")
print(f"    F1 Score:  {f1_score(y_test, y_pred_lr):.4f}")
print(f"    ROC AUC:   {roc_auc_score(y_test, y_proba_lr[:, 1]):.4f}")

print("\n  Logistic Regression Test Cases:")
print(f"    HIGH RISK: {lr_model.predict_proba(high_risk_processed)[0]}")
print(f"    LOW RISK:  {lr_model.predict_proba(low_risk_processed)[0]}")

# 11. Save models
print("\n11. Saving models...")
os.makedirs('artifacts', exist_ok=True)

# Save preprocessor
joblib.dump(preprocessor, 'artifacts/preprocessor.joblib')
print("✓ Saved preprocessor.joblib")

# Save baseline RF
joblib.dump(baseline_rf, 'artifacts/random_forest_baseline.joblib')
print("✓ Saved random_forest_baseline.joblib")

# Save tuned RF
joblib.dump(tuned_rf, 'artifacts/best_random_forest_tuned.joblib')
print("✓ Saved best_random_forest_tuned.joblib")

# Save Logistic Regression
joblib.dump(lr_model, 'artifacts/logistic_regression.joblib')
print("✓ Saved logistic_regression.joblib")

print("\n" + "="*60)
print("RETRAINING COMPLETE!")
print("="*60)
print("\nNext steps:")
print("1. Restart the API server: python api_server.py")
print("2. Test predictions in the dashboard")
print("3. Verify RF models now work correctly")
