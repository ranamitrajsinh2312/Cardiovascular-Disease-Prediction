"""
Test script to diagnose the Random Forest model issue
"""
import joblib
import pandas as pd
import numpy as np

print("="*60)
print("DIAGNOSING RANDOM FOREST MODEL ISSUE")
print("="*60)

# Load models
print("\n1. Loading models...")
try:
    preprocessor = joblib.load('artifacts/preprocessor.joblib')
    rf_model = joblib.load('artifacts/best_random_forest_tuned.joblib')
    lr_model = joblib.load('artifacts/logistic_regression.joblib')
    print("✓ Models loaded successfully")
except Exception as e:
    print(f"✗ Error loading models: {e}")
    exit(1)

# Check model types
print("\n2. Model types:")
print(f"   RF type: {type(rf_model)}")
print(f"   LR type: {type(lr_model)}")
print(f"   RF has predict_proba: {hasattr(rf_model, 'predict_proba')}")
print(f"   LR has predict_proba: {hasattr(lr_model, 'predict_proba')}")

# Create test data - HIGH RISK patient
print("\n3. Creating HIGH RISK test patient:")
high_risk_data = {
    'id': [1],
    'age': [70 * 365],  # 70 years in days
    'age_years': [70],
    'gender': [2],  # Male
    'height': [170.0],
    'weight': [115.0],  # Obese
    'ap_hi': [180],  # Very high
    'ap_lo': [80],
    'cholesterol': [3],  # Well above normal
    'gluc': [3],  # Well above normal
    'smoke': [1],  # Yes
    'alco': [1],  # Yes
    'active': [0],  # Inactive
    'cardio': [0]  # Dummy
}
df_high = pd.DataFrame(high_risk_data)
print(f"   Age: 70, Weight: 115kg, Height: 170cm")
print(f"   BP: 180/80, Chol: 3, Gluc: 3")
print(f"   Smoking: Yes, Alcohol: Yes, Inactive")

# Create test data - LOW RISK patient
print("\n4. Creating LOW RISK test patient:")
low_risk_data = {
    'id': [1],
    'age': [30 * 365],  # 30 years in days
    'age_years': [30],
    'gender': [1],  # Female
    'height': [165.0],
    'weight': [55.0],
    'ap_hi': [110],
    'ap_lo': [70],
    'cholesterol': [1],
    'gluc': [1],
    'smoke': [0],
    'alco': [0],
    'active': [1],
    'cardio': [0]
}
df_low = pd.DataFrame(low_risk_data)
print(f"   Age: 30, Weight: 55kg, Height: 165cm")
print(f"   BP: 110/70, Chol: 1, Gluc: 1")
print(f"   Smoking: No, Alcohol: No, Active")
