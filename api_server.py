"""
Flask API for ML Cardio Disease Prediction
Serves the trained ML models for predictions
"""

import logging
import os
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())

allowed_origins = [origin.strip() for origin in os.environ.get('CORS_ORIGINS', '*').split(',') if origin.strip()]
CORS(app, resources={r"/api/*": {"origins": allowed_origins}, r"/health": {"origins": allowed_origins}})

# Load models and preprocessor
BASE_DIR = Path(__file__).parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

def load_artifact(filename, required=True):
    artifact_path = ARTIFACTS_DIR / filename
    try:
        model = joblib.load(artifact_path)
        logger.info("Loaded artifact: %s", filename)
        return model
    except FileNotFoundError:
        if required:
            logger.exception("Required artifact is missing: %s", filename)
        else:
            logger.warning("Optional artifact is missing: %s", filename)
        return None


preprocessor = load_artifact("preprocessor.joblib")
rf_tuned_model = load_artifact("best_random_forest_tuned.joblib")
rf_baseline_model = load_artifact("random_forest_baseline.joblib", required=False)
lr_model = load_artifact("logistic_regression.joblib")


def models_available():
    return all(model is not None for model in (preprocessor, rf_tuned_model, lr_model))


def validate_feature_ranges(features):
    age_years = int(features.get('age_years', 45))
    height_cm = float(features.get('height', 170))
    weight_kg = float(features.get('weight', 70))
    ap_hi = float(features.get('ap_hi', 120))
    ap_lo = float(features.get('ap_lo', 80))
    cholesterol = int(features.get('cholesterol', 1))

    if not 1 <= age_years <= 120:
        raise ValueError('age_years must be between 1 and 120')
    if not 50 <= height_cm <= 250:
        raise ValueError('height must be between 50 and 250 cm')
    if not 10 <= weight_kg <= 300:
        raise ValueError('weight must be between 10 and 300 kg')
    if not 50 <= ap_hi <= 300:
        raise ValueError('ap_hi must be between 50 and 300')
    if not 30 <= ap_lo <= 200:
        raise ValueError('ap_lo must be between 30 and 200')
    if ap_hi <= ap_lo:
        raise ValueError('ap_hi must be greater than ap_lo')
    if cholesterol not in (1, 2, 3):
        raise ValueError('cholesterol must be 1, 2, or 3')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if models_available() else 'degraded',
        'models_loaded': {
            'rf_tuned': rf_tuned_model is not None,
            'rf_baseline': rf_baseline_model is not None,
            'logistic_regression': lr_model is not None
        }
    }), 200 if models_available() else 503


@app.route('/api/models/info', methods=['GET'])
def model_info():
    """Get information about available models"""
    return jsonify({
        'models': [
            {
                'id': 'rf_tuned',
                'name': 'Random Forest (Tuned)',
                'accuracy': 0.732,
                'roc_auc': 0.798,
                'precision': 0.757,
                'recall': 0.683,
                'f1': 0.718,
                'description': 'Hyperparameter-tuned Random Forest - Best Performance'
            },
            {
                'id': 'rf_baseline',
                'name': 'Random Forest (Baseline)',
                'accuracy': 0.721,
                'roc_auc': 0.783,
                'precision': 0.732,
                'recall': 0.697,
                'f1': 0.714,
                'description': 'Baseline Random Forest with default parameters',
                'available': rf_baseline_model is not None
            },
            {
                'id': 'logistic_regression',
                'name': 'Logistic Regression',
                'accuracy': 0.724,
                'roc_auc': 0.786,
                'precision': 0.746,
                'recall': 0.678,
                'f1': 0.711,
                'description': 'Fast and interpretable linear model',
                'available': lr_model is not None
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

        if not models_available():
            return jsonify({'error': 'Models are not available on the server'}), 503
        
        # Extract features
        features = data.get('features')
        model_choice = data.get('model', 'random_forest')
        validate_feature_ranges(features)
        
        # Define feature columns in the correct order (matching training data)
        # Note: New preprocessor expects BMI as an input feature
        age_in_years = int(features.get('age_years', 45))
        
        # Calculate BMI (required by new preprocessor)
        height_cm = float(features.get('height', 170))
        weight_kg = float(features.get('weight', 70))
        bmi = weight_kg / ((height_cm / 100) ** 2)
        
        # Create DataFrame with the 6 features the preprocessor expects
        feature_data = {
            'ap_hi': [float(features.get('ap_hi', 120))],
            'ap_lo': [float(features.get('ap_lo', 80))],
            'age_years': [age_in_years],
            'cholesterol': [int(features.get('cholesterol', 1))],
            'bmi': [bmi],
            'weight': [weight_kg],
        }
        feature_df = pd.DataFrame(feature_data)
        
        # Preprocess features (preprocessor will select the 6 features it needs)
        features_processed = preprocessor.transform(feature_df)
        
        # Make prediction based on model choice
        model_name = model_choice
        if model_choice == 'logistic_regression' and lr_model:
            prediction = lr_model.predict(features_processed)[0]
            probability = lr_model.predict_proba(features_processed)[0]
            model_name = 'Logistic Regression'
        elif model_choice == 'rf_baseline' and rf_baseline_model:
            prediction = rf_baseline_model.predict(features_processed)[0]
            probability = rf_baseline_model.predict_proba(features_processed)[0]
            model_name = 'Random Forest (Baseline)'
        else:  # Default to RF Tuned
            prediction = rf_tuned_model.predict(features_processed)[0]
            probability = rf_tuned_model.predict_proba(features_processed)[0]
            model_name = 'Random Forest (Tuned)'
        
        response = {
            'prediction': int(prediction),
            'probability': {
                'no_disease': float(probability[0]),
                'disease': float(probability[1])
            },
            'risk_level': 'High' if probability[1] > 0.7 else 'Medium' if probability[1] > 0.4 else 'Low',
            'confidence': float(max(probability) * 100),
            'model_used': model_name
        }
        
        return jsonify(response)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    
    except Exception as e:
        logger.exception("Prediction error")
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

        if not models_available():
            return jsonify({'error': 'Models are not available on the server'}), 503
        
        samples = data.get('samples', [])
        predictions = []
        
        for idx, features in enumerate(samples):
            validate_feature_ranges(features)
            age_in_years = int(features.get('age_years', 45))
            
            # Calculate BMI (required by new preprocessor)
            height_cm = float(features.get('height', 170))
            weight_kg = float(features.get('weight', 70))
            bmi = weight_kg / ((height_cm / 100) ** 2)
            
            # Create DataFrame with the 6 features the preprocessor expects
            feature_data = {
                'ap_hi': [float(features.get('ap_hi', 120))],
                'ap_lo': [float(features.get('ap_lo', 80))],
                'age_years': [age_in_years],
                'cholesterol': [int(features.get('cholesterol', 1))],
                'bmi': [bmi],
                'weight': [weight_kg],
            }
            feature_df = pd.DataFrame(feature_data)
            
            if preprocessor:
                features_processed = preprocessor.transform(feature_df)
            else:
                features_processed = feature_df.values
            
            prediction = rf_tuned_model.predict(features_processed)[0]
            probability = rf_tuned_model.predict_proba(features_processed)[0]
            
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
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    
    except Exception as e:
        logger.exception("Batch prediction error")
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
            'features': 6,
            'feature_names': ['ap_hi', 'ap_lo', 'age_years', 'cholesterol', 'bmi', 'weight'],
            'target': 'cardio (binary classification)'
        }
    })


@app.route('/api/feature/importance', methods=['GET'])
def feature_importance():
    """Get feature importance from the best model"""
    try:
        if hasattr(rf_tuned_model, 'feature_importances_'):
            importances = rf_tuned_model.feature_importances_
            features = ['ap_hi', 'ap_lo', 'age_years', 'cholesterol', 'bmi', 'weight']
            
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
    port = int(os.environ.get('PORT', 5000))
    logger.info("Starting ML Cardio API Server on port %s", port)
    app.run(debug=False, host='0.0.0.0', port=port)
