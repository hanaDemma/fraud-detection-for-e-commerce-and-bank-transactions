from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure logging
handler = RotatingFileHandler('logs/api.log', maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Load models
try:
    creditcard_model = joblib.load('models/logistic_regression.pkl')
    frauddata_model = load_model('models/random_forest.pkl')
    app.logger.info("Successfully loaded all models")
except Exception as e:
    app.logger.error(f"Error loading models: {str(e)}")
    raise e

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint for health checks"""
    app.logger.info("Health check requested")
    return jsonify({"status": "healthy"}), 200

@app.route('/predict/creditcard', methods=['POST'])
def predict_creditcard():
    """Endpoint for credit card fraud predictions"""
    try:
        app.logger.info("Credit card prediction request received")
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1)
        
        # Preprocessing (add your specific steps)
        # ...
        
        prediction = creditcard_model.predict_proba(features)[0][1]
        result = {"fraud_probability": float(prediction)}
        
        app.logger.info(f"Prediction successful: {result}")
        return jsonify(result), 200
    
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/predict/frauddata', methods=['POST'])
def predict_frauddata():
    """Endpoint for general fraud predictions"""
    try:
        app.logger.info("Fraudata prediction request received")
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1)
        
        # Preprocessing for NN model
        features = (features - np.array([0.1, 0.5, ...])) / np.array([0.3, 0.8, ...])  # Example normalization
        
        prediction = frauddata_model.predict(features)[0][0]
        result = {"fraud_probability": float(prediction)}
        
        app.logger.info(f"NN prediction successful: {result}")
        return jsonify(result), 200
    
    except Exception as e:
        app.logger.error(f"NN prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)