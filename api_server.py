"""
Flask API for ML Cardio Disease Prediction
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
        # Note: Preprocessor was trained with age (in days), not age_years
        age_in_years = int(features.get('age_years', 45))
        age_in_days = age_in_years * 365  # Convert back to days as preprocessor expects
        
        # Create DataFrame for preprocessing
        feature_data = {
            'id': [1],  # Dummy id
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
    print("🚀 Starting ML Cardio API Server...")
    print("📊 Available endpoints:")
    print("  GET  /health - Health check")
    print("  GET  /api/models/info - Model information")
    print("  GET  /api/model/metrics - Detailed model metrics")
    print("  GET  /api/feature/importance - Feature importance")
    print("  POST /api/predict - Single prediction")
    print("  POST /api/predict/batch - Batch predictions")
    print("\n🌐 Server running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
