import logging
import os
from pathlib import Path

from flask import Flask, jsonify, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / 'artifacts'


def load_artifact(filename, required=True):
    artifact_path = ARTIFACTS_DIR / filename
    try:
        model = joblib.load(artifact_path)
        logger.info('Loaded artifact: %s', filename)
        return model
    except FileNotFoundError:
        if required:
            logger.exception('Required artifact is missing: %s', filename)
        else:
            logger.warning('Optional artifact is missing: %s', filename)
        return None


def _patch_logistic_regression(model):
    """Ensure legacy LogisticRegression models have required attributes.

    Matches the compatibility fix used in the main api_server so that
    existing logistic_regression.joblib artifacts continue working even
    if they were trained with an older scikit-learn version.
    """
    if model is None:
        return None

    try:
        from sklearn.linear_model import LogisticRegression  # type: ignore
    except Exception:
        return model

    if isinstance(model, LogisticRegression) and not hasattr(model, 'multi_class'):
        try:
            default_multi_class = LogisticRegression().multi_class
        except Exception:
            default_multi_class = 'ovr'
        setattr(model, 'multi_class', default_multi_class)
        logger.warning(
            "Patched LogisticRegression model: added missing 'multi_class' attribute (set to %s)",
            default_multi_class,
        )

    return model


preprocessor = load_artifact('preprocessor.joblib')
rf_tuned_model = load_artifact('best_random_forest_tuned.joblib')
rf_baseline_model = load_artifact('random_forest_baseline.joblib', required=False)
lr_model = _patch_logistic_regression(load_artifact('logistic_regression.joblib'))


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


def build_feature_frame(features):
    age_in_years = int(features.get('age_years', 45))
    height_cm = float(features.get('height', 170))
    weight_kg = float(features.get('weight', 70))
    bmi = weight_kg / ((height_cm / 100) ** 2)

    return pd.DataFrame({
        'ap_hi': [float(features.get('ap_hi', 120))],
        'ap_lo': [float(features.get('ap_lo', 80))],
        'age_years': [age_in_years],
        'cholesterol': [int(features.get('cholesterol', 1))],
        'bmi': [bmi],
        'weight': [weight_kg],
    })


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy' if models_available() else 'degraded',
        'models_loaded': {
            'rf_tuned': rf_tuned_model is not None,
            'rf_baseline': rf_baseline_model is not None,
            'logistic_regression': lr_model is not None,
        }
    }), 200 if models_available() else 503


@app.route('/api/models/info', methods=['GET'])
def model_info():
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
                'description': 'Hyperparameter-tuned Random Forest - Best Performance',
                'available': rf_tuned_model is not None,
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
                'available': rf_baseline_model is not None,
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
                'available': lr_model is not None,
            }
        ]
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data or 'features' not in data:
            return jsonify({'error': 'Missing features in request'}), 400

        if not models_available():
            return jsonify({'error': 'Models are not available on the server'}), 503

        features = data.get('features')
        model_choice = data.get('model', 'random_forest')
        validate_feature_ranges(features)

        feature_df = build_feature_frame(features)
        features_processed = preprocessor.transform(feature_df)

        model_name = model_choice
        if model_choice == 'logistic_regression' and lr_model:
            prediction = lr_model.predict(features_processed)[0]
            probability = lr_model.predict_proba(features_processed)[0]
            model_name = 'Logistic Regression'
        elif model_choice == 'rf_baseline' and rf_baseline_model:
            prediction = rf_baseline_model.predict(features_processed)[0]
            probability = rf_baseline_model.predict_proba(features_processed)[0]
            model_name = 'Random Forest (Baseline)'
        else:
            prediction = rf_tuned_model.predict(features_processed)[0]
            probability = rf_tuned_model.predict_proba(features_processed)[0]
            model_name = 'Random Forest (Tuned)'

        return jsonify({
            'prediction': int(prediction),
            'probability': {
                'no_disease': float(probability[0]),
                'disease': float(probability[1]),
            },
            'risk_level': 'High' if probability[1] > 0.7 else 'Medium' if probability[1] > 0.4 else 'Low',
            'confidence': float(max(probability) * 100),
            'model_used': model_name,
        })
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    except Exception as error:
        logger.exception('Prediction error')
        return jsonify({'error': str(error)}), 500


@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    try:
        data = request.get_json()

        if not data or 'samples' not in data:
            return jsonify({'error': 'Missing samples in request'}), 400

        if not models_available():
            return jsonify({'error': 'Models are not available on the server'}), 503

        predictions = []

        for features in data.get('samples', []):
            validate_feature_ranges(features)
            feature_df = build_feature_frame(features)
            features_processed = preprocessor.transform(feature_df)
            prediction = rf_tuned_model.predict(features_processed)[0]
            probability = rf_tuned_model.predict_proba(features_processed)[0]

            predictions.append({
                'prediction': int(prediction),
                'probability': {
                    'no_disease': float(probability[0]),
                    'disease': float(probability[1]),
                },
                'confidence': float(max(probability) * 100),
            })

        return jsonify({
            'predictions': predictions,
            'total': len(predictions),
            'positive_cases': sum(1 for item in predictions if item['prediction'] == 1),
        })
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    except Exception as error:
        logger.exception('Batch prediction error')
        return jsonify({'error': str(error)}), 500


@app.route('/api/model/metrics', methods=['GET'])
def model_metrics():
    return jsonify({
        'best_model': {
            'name': 'Random Forest (Tuned)',
            'hyperparameters': {
                'n_estimators': 200,
                'max_depth': 10,
                'min_samples_split': 2,
            },
            'metrics': {
                'accuracy': 0.732,
                'precision': 0.757,
                'recall': 0.683,
                'f1': 0.718,
                'roc_auc': 0.798,
            },
            'cv_stability': {
                'mean_roc_auc': 0.7864,
                'std': 0.0026,
            }
        },
        'training_info': {
            'dataset': 'cardio_train_properly_separated_comma.csv',
            'total_samples': 70000,
            'train_samples': 56000,
            'test_samples': 14000,
            'features': 6,
            'feature_names': ['ap_hi', 'ap_lo', 'age_years', 'cholesterol', 'bmi', 'weight'],
            'target': 'cardio (binary classification)',
        }
    })


@app.route('/api/feature/importance', methods=['GET'])
def feature_importance():
    try:
        if not hasattr(rf_tuned_model, 'feature_importances_'):
            return jsonify({'error': 'Model does not support feature importance'}), 400

        importances = rf_tuned_model.feature_importances_
        features = ['ap_hi', 'ap_lo', 'age_years', 'cholesterol', 'bmi', 'weight']
        sorted_idx = np.argsort(importances)[::-1]

        return jsonify({
            'features': [features[index] for index in sorted_idx],
            'importance': [float(importances[index]) for index in sorted_idx],
            'top_5': {
                'features': [features[index] for index in sorted_idx[:5]],
                'importance': [float(importances[index]) for index in sorted_idx[:5]],
            }
        })
    except Exception as error:
        return jsonify({'error': str(error)}), 500


@app.errorhandler(404)
def not_found(_error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(_error):
    return jsonify({'error': 'Internal server error'}), 500