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
    'weight': [60.0],  # Normal
    'ap_hi': [110],  # Normal
    'ap_lo': [70],
    'cholesterol': [1],  # Normal
    'gluc': [1],  # Normal
    'smoke': [0],  # No
    'alco': [0],  # No
    'active': [1],  # Active
    'cardio': [0]  # Dummy
}
df_low = pd.DataFrame(low_risk_data)
print(f"   Age: 30, Weight: 60kg, Height: 165cm")
print(f"   BP: 110/70, Chol: 1, Gluc: 1")
print(f"   No smoking, No alcohol, Active")

# Preprocess
print("\n5. Preprocessing data...")
X_high = preprocessor.transform(df_high)
X_low = preprocessor.transform(df_low)
print(f"   Preprocessed shape: {X_high.shape}")

# Test RF model
print("\n6. Random Forest predictions:")
print("\n   HIGH RISK patient:")
rf_pred_high = rf_model.predict(X_high)[0]
rf_proba_high = rf_model.predict_proba(X_high)[0]
print(f"   Prediction: {rf_pred_high} (0=No Disease, 1=Disease)")
print(f"   Probabilities: [No Disease: {rf_proba_high[0]:.4f}, Disease: {rf_proba_high[1]:.4f}]")

print("\n   LOW RISK patient:")
rf_pred_low = rf_model.predict(X_low)[0]
rf_proba_low = rf_model.predict_proba(X_low)[0]
print(f"   Prediction: {rf_pred_low} (0=No Disease, 1=Disease)")
print(f"   Probabilities: [No Disease: {rf_proba_low[0]:.4f}, Disease: {rf_proba_low[1]:.4f}]")

# Test LR model
print("\n7. Logistic Regression predictions:")
print("\n   HIGH RISK patient:")
lr_pred_high = lr_model.predict(X_high)[0]
lr_proba_high = lr_model.predict_proba(X_high)[0]
print(f"   Prediction: {lr_pred_high} (0=No Disease, 1=Disease)")
print(f"   Probabilities: [No Disease: {lr_proba_high[0]:.4f}, Disease: {lr_proba_high[1]:.4f}]")

print("\n   LOW RISK patient:")
lr_pred_low = lr_model.predict(X_low)[0]
lr_proba_low = lr_model.predict_proba(X_low)[0]
print(f"   Prediction: {lr_pred_low} (0=No Disease, 1=Disease)")
print(f"   Probabilities: [No Disease: {lr_proba_low[0]:.4f}, Disease: {lr_proba_low[1]:.4f}]")

# Check if RF is stuck
print("\n8. Diagnosis:")
if rf_pred_high == rf_pred_low:
    print("   ⚠️  WARNING: RF model predicting same class for both patients!")
    print("   This suggests the model might be stuck or corrupted.")
else:
    print("   ✓ RF model is differentiating between patients")

if rf_proba_high[1] < 0.5 and lr_proba_high[1] > 0.5:
    print("   ⚠️  RF predicting LOW risk for HIGH risk patient!")
    print("   ⚠️  LR correctly predicting HIGH risk")
    print("\n   ISSUE IDENTIFIED: Random Forest model is not working correctly")
    print("   Possible causes:")
    print("   - Model was trained on different features")
    print("   - Model file is corrupted")
    print("   - Wrong model was saved to best_random_forest_tuned.joblib")
elif rf_proba_high[1] > 0.7:
    print("   ✓ RF correctly predicting HIGH risk for HIGH risk patient")

print("\n" + "="*60)
print("DIAGNOSIS COMPLETE")
print("="*60)
