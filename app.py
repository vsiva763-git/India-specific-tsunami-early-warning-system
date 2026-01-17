#!/usr/bin/env python3
"""
Flask API for Tsunami Detection Model
REST API endpoint for real-time tsunami prediction
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load model
MODEL_PATH = Path('./tsunami_detection_binary_focal.keras')
METADATA_PATH = Path('./model_metadata.json')

try:
    model = tf.keras.models.load_model(str(MODEL_PATH))
    logger.info(f"✓ Model loaded from {MODEL_PATH}")
except Exception as e:
    logger.error(f"✗ Failed to load model: {e}")
    model = None

# Load metadata
try:
    with open(METADATA_PATH, 'r') as f:
        metadata = json.load(f)
    logger.info(f"✓ Metadata loaded from {METADATA_PATH}")
except Exception as e:
    logger.error(f"✗ Failed to load metadata: {e}")
    metadata = None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_type': metadata.get('model_type') if metadata else None
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict tsunami probability
    
    Expected input:
    {
        "data": [[timestep1_features], [timestep2_features], ...],
        "threshold": 0.1  // optional
    }
    
    Input shape: (24, 32) - 24 timesteps, 32 features
    """
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get request data
        request_data = request.get_json()
        
        if 'data' not in request_data:
            return jsonify({'error': 'Missing "data" field'}), 400
        
        # Parse input
        input_data = np.array(request_data['data'], dtype=np.float32)
        threshold = request_data.get('threshold', 0.1)
        
        # Validate input shape
        if input_data.ndim == 2:
            # Single sample: (24, 32)
            input_data = np.expand_dims(input_data, axis=0)
        elif input_data.ndim != 3:
            return jsonify({'error': f'Invalid input shape. Expected (24, 32) or (batch, 24, 32), got {input_data.shape}'}), 400
        
        # Validate dimensions
        if input_data.shape[1:] != (24, 32):
            return jsonify({'error': f'Expected features (24, 32), got {input_data.shape[1:]}'}), 400
        
        # Make prediction
        predictions = model.predict(input_data, verbose=0)
        probabilities = predictions.flatten().tolist()
        
        # Apply threshold
        alerts = [float(p > threshold) for p in probabilities]
        
        return jsonify({
            'success': True,
            'probabilities': probabilities,
            'alerts': alerts,
            'threshold': threshold,
            'interpretation': [
                'Tsunami detected' if alert else 'No tsunami'
                for alert in alerts
            ]
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/model-info', methods=['GET'])
def model_info():
    """Get model information and performance metrics"""
    if metadata is None:
        return jsonify({'error': 'Metadata not available'}), 500
    
    return jsonify({
        'model': metadata,
        'endpoints': {
            'predict': '/predict (POST)',
            'health': '/health (GET)',
            'model_info': '/model-info (GET)'
        }
    }), 200


@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction for multiple samples
    
    Expected input:
    {
        "samples": [
            [[timestep1_features], ...],
            [[timestep1_features], ...],
            ...
        ],
        "threshold": 0.1
    }
    """
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        request_data = request.get_json()
        
        if 'samples' not in request_data:
            return jsonify({'error': 'Missing "samples" field'}), 400
        
        # Parse batch
        samples = np.array(request_data['samples'], dtype=np.float32)
        threshold = request_data.get('threshold', 0.1)
        
        # Validate shape
        if samples.shape[1:] != (24, 32):
            return jsonify({'error': f'Expected features (24, 32) per sample, got {samples.shape[1:]}'}), 400
        
        # Batch predict
        predictions = model.predict(samples, verbose=0)
        probabilities = predictions.flatten().tolist()
        alerts = [float(p > threshold) for p in probabilities]
        
        return jsonify({
            'success': True,
            'batch_size': len(samples),
            'probabilities': probabilities,
            'alerts': alerts,
            'alert_count': sum(alerts),
            'alert_rate': f"{100 * sum(alerts) / len(alerts):.2f}%",
            'threshold': threshold
        }), 200
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/health',
            '/predict',
            '/batch-predict',
            '/model-info'
        ]
    }), 404


if __name__ == '__main__':
    logger.info("Starting Tsunami Detection API...")
    logger.info("Available endpoints:")
    logger.info("  - GET  /health")
    logger.info("  - POST /predict")
    logger.info("  - POST /batch-predict")
    logger.info("  - GET  /model-info")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
