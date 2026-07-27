"""
Flask API for ML Cardio Disease Prediction (Dashboard 2)
Serves the trained ML models for predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Load models and preprocessor
BASE_DIR = Path(__file__).parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

try:
    preprocessor = joblib.load(ARTIFACTS_DIR / "preprocessor.joblib")
    best_model = joblib.load(ARTIFACTS_DIR / "best_random_forest_tuned.joblib")
    lr_model = joblib.load(ARTIFACTS_DIR / "logistic_regression.joblib")
    print("✓ Models loaded successfully")
except FileNotFoundError as e:
    print(f"⚠ Error loading models: {e}")
    preprocessor = None
    best_model = None
    lr_model = None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': best_model is not None
    })


@app.route('/api/models/info', methods=['GET'])
def model_info():
    """Get information about available models"""
    return jsonify({
        'models': [
            {
                'name': 'Random Forest (Tuned)',
                'accuracy': 0.732,
                'roc_auc': 0.798,
                'precision': 0.757,
                'recall': 0.683,
                'f1': 0.718
            },
            {
                'name': 'Logistic Regression',
                'accuracy': 0.724,
                'roc_auc': 0.786,
                'precision': 0.746,
                'recall': 0.678,
                'f1': 0.711
            }
        ]
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict cardiovascular disease risk based on patient health data.
    
    INPUT:
    - Patient health inputs: age (years), gender, height (cm), weight (kg), 
      blood pressure (ap_hi/ap_lo), cholesterol, glucose, lifestyle factors
    
    PROCESSING:
    1. Calculate BMI: weight (kg) / (height (m)²)
    2. Preprocess data according to training dataset:
       - Encode categorical values (gender, cholesterol, glucose, smoke, alco, active)
       - Scale numeric features using StandardScaler
       - Apply OneHotEncoder for categorical variables
    3. Use trained Random Forest model to predict
    4. Get prediction confidence using predict_proba
    
    OUTPUT:
    - prediction: 0 (Disease Absent) or 1 (Disease Present)
    - probability: {'no_disease': float, 'disease': float}
    - risk_level: Low/Medium/High classification
      * Low: probability < 40%
      * Medium: probability 40-70%
      * High: probability > 70%
    - confidence: Confidence score as percentage
    
    Expected JSON format:
    {
        "model": "random_forest",
        "features": {
            "age_years": 45,
            "weight": 70,
            "height": 170,
            "gender": 1,
            "cholesterol": 1,
            "gluc": 1,
            "ap_hi": 120,
            "ap_lo": 80,
            "smoke": 0,
            "alco": 0,
            "active": 1,
            "bmi": 24.2
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({'error': 'Missing features in request'}), 400
        
        # Extract features
        features = data.get('features')
        model_choice = data.get('model', 'random_forest')
        
        # Define feature columns in the correct order (matching training data)
        # Note: Preprocessor was trained with age_years, not age in days
        age_in_years = int(features.get('age_years', 45))
        
        # Calculate BMI from the features if not provided
        height_m = float(features.get('height', 170)) / 100
        weight_kg = float(features.get('weight', 70))
        calculated_bmi = weight_kg / (height_m * height_m)
        
        # Create DataFrame for preprocessing
        feature_data = {
            'id': [1],  # Dummy id
            'age': [age_in_years * 365],  # Age in days (original column)
            'age_years': [age_in_years],  # Age in years (derived column)
            'gender': [int(features.get('gender', 1))],
            'height': [float(features.get('height', 170))],
            'weight': [float(features.get('weight', 70))],
            'ap_hi': [float(features.get('ap_hi', 120))],
            'ap_lo': [float(features.get('ap_lo', 80))],
            'cholesterol': [int(features.get('cholesterol', 1))],
            'gluc': [int(features.get('gluc', 1))],
            'smoke': [int(features.get('smoke', 0))],
            'alco': [int(features.get('alco', 0))],
            'active': [int(features.get('active', 1))],
            'bmi': [calculated_bmi],  # Calculate BMI for the model
            'cardio': [0],  # Dummy target variable
        }
        feature_df = pd.DataFrame(feature_data)
        
        print(f"📊 Prediction request - Features DataFrame:\n{feature_df}")
        
        # Preprocess features
        if preprocessor:
            features_processed = preprocessor.transform(feature_df)
        else:
            features_processed = feature_df.values
        
        # Make prediction
        if model_choice == 'logistic_regression' and lr_model:
            prediction = lr_model.predict(features_processed)[0]
            probability = lr_model.predict_proba(features_processed)[0]
        else:
            prediction = best_model.predict(features_processed)[0]
            probability = best_model.predict_proba(features_processed)[0]
        
        response = {
            'prediction': int(prediction),
            'probability': {
                'no_disease': float(probability[0]),
                'disease': float(probability[1])
            },
            'risk_level': 'High' if probability[1] > 0.7 else 'Medium' if probability[1] > 0.4 else 'Low',
            'confidence': float(max(probability) * 100)
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/compare', methods=['POST'])
def predict_compare():
    """
    Compare predictions between tuned and baseline models
    
    Expected JSON format:
    {
        "features": {
            "age_years": 45,
            "weight": 70,
            "height": 170,
            "gender": 1,
            "cholesterol": 1,
            "gluc": 1,
            "ap_hi": 120,
            "ap_lo": 80,
            "smoke": 0,
            "alco": 0,
            "active": 1,
            "bmi": 24.2
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({'error': 'Missing features in request'}), 400
        
        # Extract features
        features = data.get('features')
        
        # Define feature columns in the correct order (matching training data)
        age_in_years = int(features.get('age_years', 45))
        age_in_days = age_in_years * 365  # Convert back to days as preprocessor expects
        
        # Calculate BMI from the features if not provided
        height_m = float(features.get('height', 170)) / 100
        weight_kg = float(features.get('weight', 70))
        calculated_bmi = weight_kg / (height_m * height_m)
        
        # Create DataFrame for preprocessing
        # Note: The preprocessor expects both age (days) and age_years
        feature_data = {
            'id': [1],  # Dummy id
            'age': [age_in_days],  # Age in days (original column)
            'age_years': [age_in_years],  # Age in years (derived column)
            'gender': [int(features.get('gender', 1))],
            'height': [float(features.get('height', 170))],
            'weight': [float(features.get('weight', 70))],
            'ap_hi': [float(features.get('ap_hi', 120))],
            'ap_lo': [float(features.get('ap_lo', 80))],
            'cholesterol': [int(features.get('cholesterol', 1))],
            'gluc': [int(features.get('gluc', 1))],
            'smoke': [int(features.get('smoke', 0))],
            'alco': [int(features.get('alco', 0))],
            'active': [int(features.get('active', 1))],
            'bmi': [calculated_bmi],  # Calculate BMI for the model
            'cardio': [0],  # Dummy target variable
        }
        feature_df = pd.DataFrame(feature_data)
        
        print(f"📊 Compare prediction request - Features DataFrame:\n{feature_df}")
        print(f"🔍 Age: {age_in_years} years")
        print(f"🔍 BMI calculation: {weight_kg}kg / ({height_m}m)² = {calculated_bmi:.2f}")
        
        # Preprocess features
        if preprocessor:
            features_processed = preprocessor.transform(feature_df)
            print(f"🔍 Raw features shape: {feature_df.shape}")
            print(f"🔍 Processed features shape: {features_processed.shape}")
            print(f"🔍 First 10 processed features: {features_processed[0][:10]}")
            print(f"🔍 All processed features: {features_processed[0]}")
        else:
            features_processed = feature_df.values
            print(f"⚠ No preprocessor - using raw values")
        
        # Get predictions from tuned model first
        tuned_prediction = best_model.predict(features_processed)[0]
        tuned_probability = best_model.predict_proba(features_processed)[0]
        
        # Medical Risk Adjustment - Override model for obvious high-risk cases
        def apply_medical_risk_adjustment(prediction, probability, features):
            """Apply medical knowledge to adjust obviously wrong predictions"""
            age = features.get('age_years', 45)
            systolic = features.get('ap_hi', 120)
            diastolic = features.get('ap_lo', 80)
            smoking = features.get('smoke', 0)
            alcohol = features.get('alco', 0)
            
            # Calculate risk score based on medical guidelines
            risk_score = 0
            
            # Age risk (higher after 45 for men, 55 for women)
            if age >= 55: risk_score += 25
            elif age >= 50: risk_score += 15
            elif age >= 45: risk_score += 10
            
            # Blood pressure risk (AHA guidelines)
            if systolic >= 180 or diastolic >= 110: risk_score += 40  # Stage 2 Hypertension
            elif systolic >= 160 or diastolic >= 100: risk_score += 30  # Stage 2
            elif systolic >= 140 or diastolic >= 90: risk_score += 20   # Stage 1
            elif systolic >= 130 or diastolic >= 80: risk_score += 10   # Elevated
            
            # Lifestyle risk factors
            if smoking: risk_score += 15  # Reduced from 25 - moderate risk factor
            if alcohol: risk_score += 5   # Reduced from 10 - mild risk factor
            
            # If medical risk score indicates high risk but model says low risk, adjust
            if risk_score >= 60 and probability[1] < 0.4:
                print(f"🏥 Medical Override: Risk score {risk_score}% - adjusting from {probability[1]*100:.1f}% to 65%")
                adjusted_prob = [0.35, 0.65]  # High risk
                return 1, adjusted_prob, f"High (Medical Override - Risk Score: {risk_score}%)"
            elif risk_score >= 40 and probability[1] < 0.3:
                print(f"🏥 Medical Override: Risk score {risk_score}% - adjusting from {probability[1]*100:.1f}% to 50%")
                adjusted_prob = [0.50, 0.50]  # Medium-High risk
                return 1, adjusted_prob, f"Medium-High (Medical Override - Risk Score: {risk_score}%)"
            elif risk_score >= 25 and probability[1] < 0.2:
                print(f"🏥 Medical Override: Risk score {risk_score}% - adjusting from {probability[1]*100:.1f}% to 35%")
                adjusted_prob = [0.65, 0.35]  # Medium risk
                return 0, adjusted_prob, f"Medium (Medical Override - Risk Score: {risk_score}%)"
            
            # No adjustment needed
            risk_level = 'High' if probability[1] > 0.7 else 'Medium' if probability[1] > 0.4 else 'Low'
            return prediction, probability, risk_level
        
        # Apply medical adjustment to tuned model
        tuned_prediction, tuned_probability, tuned_risk_level = apply_medical_risk_adjustment(
            tuned_prediction, tuned_probability, features
        )
        
        # Load the actual baseline model instead of using the same model
        try:
            baseline_model = joblib.load(ARTIFACTS_DIR / "random_forest_baseline_final.joblib")
            baseline_prediction = baseline_model.predict(features_processed)[0]
            baseline_probability = baseline_model.predict_proba(features_processed)[0]
            print(f"🔍 Using separate baseline model")
            
            # Apply medical adjustment to baseline model too
            baseline_prediction, baseline_probability, baseline_risk_level = apply_medical_risk_adjustment(
                baseline_prediction, baseline_probability, features
            )
        except FileNotFoundError:
            print(f"⚠ Baseline model not found, using tuned model for baseline")
            baseline_prediction = tuned_prediction
            baseline_probability = tuned_probability
            baseline_risk_level = tuned_risk_level
        
        print(f"🔍 Debug - Age: {age_in_years}, BP: {features['ap_hi']}/{features['ap_lo']}, BMI: {calculated_bmi:.2f}")
        print(f"🔍 Risk factors: Smoking={features.get('smoke')}, Alcohol={features.get('alco')}, Cholesterol={features.get('cholesterol')}")
        print(f"🔍 Tuned prediction: {tuned_prediction}, probability: {tuned_probability}")
        print(f"🔍 Disease probability: {tuned_probability[1]*100:.2f}%")
        
        # Check if the model has feature importance
        if hasattr(best_model, 'feature_importances_'):
            print(f"🔍 Model feature importances (top 5): {best_model.feature_importances_[:5]}")
        
        print(f"🔍 Baseline prediction: {baseline_prediction}, probability: {baseline_probability}")
        
        # Create response
        response = {
            'tuned_model': {
                'name': 'Random Forest (Tuned)',
                'prediction': int(tuned_prediction),
                'probability': {
                    'no_disease': float(tuned_probability[0]),
                    'disease': float(tuned_probability[1])
                },
                'risk_level': tuned_risk_level,
                'confidence': float(max(tuned_probability) * 100)
            },
            'baseline_model': {
                'name': 'Random Forest (Baseline)',
                'prediction': int(baseline_prediction),
                'probability': {
                    'no_disease': float(baseline_probability[0]),
                    'disease': float(baseline_probability[1])
                },
                'risk_level': baseline_risk_level,
                'confidence': float(max(baseline_probability) * 100)
            },
            'agreement': bool(tuned_prediction == baseline_prediction),
            'sanitized_features': features
        }
        
        print(f"📤 API Response: {response}")
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Compare prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """
    Make predictions on multiple samples
    
    Expected JSON format:
    {
        "samples": [
            {"age_years": 45, "weight": 70, ...},
            {"age_years": 50, "weight": 75, ...}
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'samples' not in data:
            return jsonify({'error': 'Missing samples in request'}), 400
        
        samples = data.get('samples', [])
        predictions = []
        
        for idx, features in enumerate(samples):
            age_in_years = int(features.get('age_years', 45))
            age_in_days = age_in_years * 365  # Convert back to days as preprocessor expects
            
            feature_data = {
                'id': [idx + 1],
                'age': [age_in_days],  # Age in days (preprocessor was trained on original age column)
                'age_years': [age_in_years],  # Age in years (created during training)
                'gender': [int(features.get('gender', 1))],
                'height': [float(features.get('height', 170))],
                'weight': [float(features.get('weight', 70))],
                'ap_hi': [float(features.get('ap_hi', 120))],
                'ap_lo': [float(features.get('ap_lo', 80))],
                'cholesterol': [int(features.get('cholesterol', 1))],
                'gluc': [int(features.get('gluc', 1))],
                'smoke': [int(features.get('smoke', 0))],
                'alco': [int(features.get('alco', 0))],
                'active': [int(features.get('active', 1))],
                'cardio': [0],
            }
            feature_df = pd.DataFrame(feature_data)
            
            if preprocessor:
                features_processed = preprocessor.transform(feature_df)
            else:
                features_processed = feature_df.values
            
            prediction = best_model.predict(features_processed)[0]
            probability = best_model.predict_proba(features_processed)[0]
            
            predictions.append({
                'prediction': int(prediction),
                'probability': {
                    'no_disease': float(probability[0]),
                    'disease': float(probability[1])
                },
                'confidence': float(max(probability) * 100)
            })
        
        return jsonify({
            'predictions': predictions,
            'total': len(predictions),
            'positive_cases': sum(1 for p in predictions if p['prediction'] == 1)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/model/metrics', methods=['GET'])
def model_metrics():
    """Get detailed model metrics"""
    return jsonify({
        'best_model': {
            'name': 'Random Forest (Tuned)',
            'hyperparameters': {
                'n_estimators': 200,
                'max_depth': 10,
                'min_samples_split': 2
            },
            'metrics': {
                'accuracy': 0.732,
                'precision': 0.757,
                'recall': 0.683,
                'f1': 0.718,
                'roc_auc': 0.798
            },
            'cv_stability': {
                'mean_roc_auc': 0.7864,
                'std': 0.0026
            }
        },
        'training_info': {
            'dataset': 'cardio_train_properly_separated_comma.csv',
            'total_samples': 70000,
            'train_samples': 56000,
            'test_samples': 14000,
            'features': 12,
            'target': 'cardio (binary classification)'
        }
    })


@app.route('/api/feature/importance', methods=['GET'])
def feature_importance():
    """Get feature importance from the best model"""
    try:
        if hasattr(best_model, 'feature_importances_'):
            importances = best_model.feature_importances_
            features = [f'Feature_{i}' for i in range(len(importances))]
            
            # Sort by importance
            sorted_idx = np.argsort(importances)[::-1]
            
            return jsonify({
                'features': [features[i] for i in sorted_idx],
                'importance': [float(importances[i]) for i in sorted_idx],
                'top_5': {
                    'features': [features[i] for i in sorted_idx[:5]],
                    'importance': [float(importances[i]) for i in sorted_idx[:5]]
                }
            })
        else:
            return jsonify({'error': 'Model does not support feature importance'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting ML Cardio API Server (Dashboard 2)...")
    print("📊 Available endpoints:")
    print("  GET  /health - Health check")
    print("  GET  /api/models/info - Model information")
    print("  GET  /api/model/metrics - Detailed model metrics")
    print("  GET  /api/feature/importance - Feature importance")
    print("  POST /api/predict - Single prediction")
    print("  POST /api/predict/compare - Compare tuned vs baseline models")
    print("  POST /api/predict/batch - Batch predictions")
    print("\n🌐 Server running on http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
