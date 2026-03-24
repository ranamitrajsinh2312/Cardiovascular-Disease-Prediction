from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/models/info', methods=['GET'])
def get_models_info():
    # Sample data for demonstration purposes
    models_info = [
        {
            "name": "Logistic Regression",
            "accuracy": 0.724,
            "precision": 0.746,
            "recall": 0.678,
            "f1": 0.711,
            "roc_auc": 0.786
        },
        {
            "name": "Random Forest (Bagging)",
            "accuracy": 0.721,
            "precision": 0.732,
            "recall": 0.697,
            "f1": 0.714,
            "roc_auc": 0.783
        },
        {
            "name": "Random Forest (Tuned)",
            "accuracy": 0.732,
            "precision": 0.757,
            "recall": 0.683,
            "f1": 0.718,
            "roc_auc": 0.798
        }
    ]
    return jsonify({"models": models_info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)