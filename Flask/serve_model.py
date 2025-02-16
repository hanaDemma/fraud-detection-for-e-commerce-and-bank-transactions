from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import logging
from logging.handlers import RotatingFileHandler
import os
from waitress import serve
# from serve_model import app  # Import your Flask app
app = Flask(__name__)
CORS(app)  # Allow all origins

# Configure logging
handler = RotatingFileHandler('logs/api.log', maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Load models
try:
    bank_model = joblib.load('models/random_forest.pkl')
    ecommerce_model = joblib.load('models/random_forest.pkl')
    app.logger.info("Successfully loaded all models")
except Exception as e:
    app.logger.error(f"Error loading models: {str(e)}")
    raise e

@app.route('/')
def home():
    """Home route."""
    return render_template('index.html')  
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint for health checks."""
    app.logger.info("Health check requested")
    return jsonify({"status": "healthy"}), 200

@app.route('/bank_predict', methods=['POST'])
def bank_predict():
    """Endpoint for credit card fraud predictions."""
    try:
        app.logger.info("Credit card prediction request received")
        data = request.json
       
         # Convert JSON to DataFrame
        df = pd.DataFrame([data])
        # Preprocessing (add your specific steps)
        # ...
        # Make predictions
        
        prediction = bank_model.predict(df)
        # app.logger.info(f"Prediction successful: {result}")
        return jsonify({'prediction': int(prediction[0])})
 
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/ecommerce_predict', methods=['POST'])
def ecommerce_predict():
    try:
        # Get JSON data from the request
        data = request.json
        
        # Convert JSON to DataFrame
        df = pd.DataFrame([data])
        
        # Make predictions
        prediction = ecommerce_model.predict(df)
        
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
