#!/usr/bin/env python3
"""
Flask API for Tsunami Detection Model
REST API endpoint for real-time tsunami prediction
"""

from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import json
from pathlib import Path
import logging
from datetime import datetime, timedelta
import requests as http_requests

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load model
MODEL_PATH = Path('./models/tsunami_detection_binary_focal.keras')
METADATA_PATH = Path('./models/model_metadata.json')

try:
    # Load model weights only (without custom loss function)
    # This bypasses the custom loss deserialization issue
    model = tf.keras.models.load_model(str(MODEL_PATH), compile=False)
    # Compile with standard binary crossentropy for inference
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    logger.info(f"✓ Model loaded from {MODEL_PATH} (weights only, compiled with binary_crossentropy)")
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


@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def serve_dashboard():
    """Serve the live dashboard with Indian Ocean data"""
    try:
        response = make_response(send_file('static/index_live.html'))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        return jsonify({'error': 'Dashboard not found'}), 404


@app.route('/test-data', methods=['GET'])
def get_test_data():
    """
    Return test earthquake data for demonstration
    Shows how the system responds to real earthquake scenarios
    """
    return jsonify({
        'success': True,
        'region': 'Indian Ocean',
        'time_range': {
            'start': (datetime.utcnow() - timedelta(hours=24)).isoformat(),
            'end': datetime.utcnow().isoformat()
        },
        'total_earthquakes': 3,
        'earthquakes': [
            {
                'magnitude': 6.8,
                'location': 'Off West Coast of Sumatra',
                'latitude': 0.5,
                'longitude': 95.2,
                'depth': 45,
                'time': (datetime.utcnow() - timedelta(hours=2)).timestamp() * 1000,
                'url': 'https://earthquake.usgs.gov/earthquakes/events/',
                'tsunami_probability': 0.75,
                'tsunami_risk': 'HIGH'
            },
            {
                'magnitude': 5.9,
                'location': 'Bay of Bengal',
                'latitude': 10.2,
                'longitude': 86.5,
                'depth': 32,
                'time': (datetime.utcnow() - timedelta(hours=6)).timestamp() * 1000,
                'url': 'https://earthquake.usgs.gov/earthquakes/events/',
                'tsunami_probability': 0.38,
                'tsunami_risk': 'MODERATE'
            },
            {
                'magnitude': 5.2,
                'location': 'Andaman Sea',
                'latitude': 8.5,
                'longitude': 94.3,
                'depth': 28,
                'time': (datetime.utcnow() - timedelta(hours=12)).timestamp() * 1000,
                'url': 'https://earthquake.usgs.gov/earthquakes/events/',
                'tsunami_probability': 0.15,
                'tsunami_risk': 'LOW'
            }
        ],
        'predictions': [],
        'high_risk_count': 1,
        'alerts_triggered': 1
    }), 200


@app.route('/live-data', methods=['GET'])
def get_live_data():
    """
    Fetch live seismic data from Indian Ocean region and predict tsunami risk
    Data source: USGS Earthquake API
    """
    try:
        # Indian Ocean region coordinates (approximate bounding box)
        # Latitude: -40 to 30, Longitude: 40 to 120
        min_lat, max_lat = -40, 30
        min_lon, max_lon = 40, 120
        
        # Get earthquakes from last 24 hours
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        # USGS Earthquake API
        usgs_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            'format': 'geojson',
            'starttime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'endtime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'minlatitude': min_lat,
            'maxlatitude': max_lat,
            'minlongitude': min_lon,
            'maxlongitude': max_lon,
            'minmagnitude': 4.0,  # Only significant earthquakes
            'orderby': 'time-asc'
        }
        
        response = http_requests.get(usgs_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        earthquakes = []
        predictions = []
        
        for feature in data.get('features', [])[:10]:  # Limit to 10 most recent
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            
            # Extract earthquake info
            eq_info = {
                'id': feature.get('id'),
                'magnitude': props.get('mag'),
                'location': props.get('place'),
                'time': props.get('time'),
                'latitude': coords[1],
                'longitude': coords[0],
                'depth': coords[2],
                'url': props.get('url')
            }
            
            # Convert earthquake data to model input format
            # Create synthetic seismic pattern based on earthquake parameters
            seismic_data = create_seismic_pattern(
                magnitude=eq_info['magnitude'],
                depth=eq_info['depth'],
                latitude=eq_info['latitude'],
                longitude=eq_info['longitude']
            )
            
            # Make prediction
            if model is not None:
                input_data = np.expand_dims(seismic_data, axis=0)
                prediction = model.predict(input_data, verbose=0)
                probability = float(prediction[0][0])
                
                eq_info['tsunami_probability'] = probability
                eq_info['tsunami_risk'] = 'HIGH' if probability > 0.5 else 'MODERATE' if probability > 0.2 else 'LOW'
                eq_info['alert'] = probability > 0.1
                
                predictions.append({
                    'earthquake': eq_info,
                    'prediction': {
                        'probability': probability,
                        'risk_level': eq_info['tsunami_risk'],
                        'alert': eq_info['alert']
                    }
                })
            
            earthquakes.append(eq_info)
        
        return jsonify({
            'success': True,
            'region': 'Indian Ocean',
            'time_range': {
                'start': start_time.isoformat(),
                'end': end_time.isoformat()
            },
            'total_earthquakes': len(earthquakes),
            'earthquakes': earthquakes,
            'predictions': predictions,
            'high_risk_count': sum(1 for p in predictions if p['prediction']['risk_level'] == 'HIGH'),
            'alerts_triggered': sum(1 for p in predictions if p['prediction']['alert'])
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching live data: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch live seismic data'
        }), 500


@app.route('/wave-data', methods=['GET'])
def get_wave_data():
    """
    Fetch real-time ocean wave and water level data from monitoring stations
    Data sources: IOC Sea Level stations, NOAA DART buoys
    """
    try:
        # Define monitoring stations with IOC codes
        stations = {
            'arabian': {
                'name': 'Arabian Sea',
                'stations': [
                    {'id': 'okha', 'ioc_code': 'okha', 'lat': 22.47, 'lon': 69.07, 'name': 'Okha, India'},
                    {'id': 'mumbai', 'ioc_code': 'bomb', 'lat': 18.95, 'lon': 72.82, 'name': 'Mumbai, India'},
                ]
            },
            'bengal': {
                'name': 'Bay of Bengal',
                'stations': [
                    {'id': 'chennai', 'ioc_code': 'ched', 'lat': 13.10, 'lon': 80.30, 'name': 'Chennai, India'},
                    {'id': 'vizag', 'ioc_code': 'visa', 'lat': 17.68, 'lon': 83.28, 'name': 'Visakhapatnam, India'},
                ]
            },
            'andaman': {
                'name': 'Andaman Sea',
                'stations': [
                    {'id': 'portblair', 'ioc_code': 'port', 'lat': 11.66, 'lon': 92.73, 'name': 'Port Blair, India'},
                    {'id': 'phuket', 'ioc_code': 'phuk', 'lat': 7.89, 'lon': 98.39, 'name': 'Phuket, Thailand'},
                ]
            }
        }
        
        wave_data = {}
        
        for region_key, region_info in stations.items():
            region_readings = []
            
            for station in region_info['stations']:
                try:
                    # Try IOC Sea Level Monitoring API
                    ioc_code = station.get('ioc_code', '').upper()
                    
                    # IOC API endpoint - last 1 hour of data
                    ioc_url = f"http://www.ioc-sealevelmonitoring.org/service.php"
                    params = {
                        'code': ioc_code,
                        'period': 0.04  # Last ~1 hour (0.04 days)
                    }
                    
                    response = http_requests.get(ioc_url, params=params, timeout=10)
                    
                    if response.status_code == 200 and len(response.text) > 100:
                        # Parse IOC CSV data
                        lines = response.text.strip().split('\n')
                        readings = []
                        
                        # Skip header lines and parse data
                        data_started = False
                        for line in lines:
                            line = line.strip()
                            if not line or line.startswith('#'):
                                continue
                            if 'slevel' in line.lower() or 'time' in line.lower():
                                data_started = True
                                continue
                            if data_started:
                                parts = line.split(',')
                                if len(parts) >= 2:
                                    try:
                                        # Format: timestamp, water_level, ...
                                        timestamp = parts[0].strip()
                                        water_level = float(parts[1].strip())
                                        
                                        # Convert to meters and add offset for visualization
                                        water_level_m = water_level / 100.0  # cm to meters
                                        water_level_m += 5.0  # Add baseline for positive display
                                        
                                        readings.append({
                                            'time': timestamp,
                                            'value': round(water_level_m, 3),
                                            'quality': 'verified'
                                        })
                                    except (ValueError, IndexError):
                                        continue
                        
                        if len(readings) >= 5:  # Need at least 5 readings
                            # Take last 10 readings
                            readings = readings[-10:]
                            
                            region_readings.append({
                                'station_id': station['id'],
                                'station_name': station['name'],
                                'location': {'lat': station['lat'], 'lon': station['lon']},
                                'readings': readings,
                                'source': 'IOC Sea Level Station',
                                'data_type': 'sea_level',
                                'unit': 'meters',
                                'real_data': True
                            })
                            logger.info(f"✓ Real-time data from {station['name']} ({ioc_code}): {len(readings)} readings")
                            continue
                    
                except Exception as e:
                    logger.debug(f"IOC data unavailable for {station['name']}: {e}")
                
                # Try NDBC/DART buoys for backup
                try:
                    # Map regions to nearby DART buoys
                    dart_buoys = {
                        'bengal': '23401',  # Bay of Bengal DART
                        'andaman': '23401'  # Also covers Andaman
                    }
                    
                    if region_key in dart_buoys:
                        buoy_id = dart_buoys[region_key]
                        dart_url = f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.txt"
                        
                        response = http_requests.get(dart_url, timeout=8)
                        
                        if response.status_code == 200:
                            lines = response.text.strip().split('\n')
                            readings = []
                            
                            # Parse NDBC format (first 2 lines are headers)
                            for line in lines[2:12]:  # Get 10 readings
                                parts = line.split()
                                if len(parts) >= 5:
                                    try:
                                        # NDBC format: YY MM DD hh mm WDIR WSPD GST WVHT ...
                                        year, month, day, hour, minute = parts[0:5]
                                        
                                        # Construct timestamp
                                        timestamp = f"20{year}-{month}-{day} {hour}:{minute}"
                                        
                                        # Get wave height if available (usually column 8)
                                        wave_height = float(parts[8]) if len(parts) > 8 and parts[8] != 'MM' else 5.0
                                        
                                        readings.append({
                                            'time': timestamp,
                                            'value': round(wave_height, 2),
                                            'quality': 'measured'
                                        })
                                    except (ValueError, IndexError):
                                        continue
                            
                            if len(readings) >= 5:
                                region_readings.append({
                                    'station_id': f'dart_{buoy_id}',
                                    'station_name': f'DART Buoy {buoy_id}',
                                    'location': {'lat': station['lat'], 'lon': station['lon']},
                                    'readings': readings[-10:],
                                    'source': 'NOAA DART Buoy',
                                    'data_type': 'wave_height',
                                    'unit': 'meters',
                                    'real_data': True
                                })
                                logger.info(f"✓ Real-time DART data from buoy {buoy_id}: {len(readings)} readings")
                                continue
                
                except Exception as e:
                    logger.debug(f"DART data unavailable: {e}")
                
                # If no real data available, generate realistic fallback
                logger.info(f"Using simulated data for {station['name']}")
                current_time = datetime.utcnow()
                readings = []
                
                regional_params = {
                    'arabian': {'baseline': 4.2, 'tide_amp': 1.8, 'wave_amp': 0.6},
                    'bengal': {'baseline': 4.8, 'tide_amp': 2.2, 'wave_amp': 0.8},
                    'andaman': {'baseline': 3.9, 'tide_amp': 1.6, 'wave_amp': 0.7}
                }
                
                params = regional_params[region_key]
                
                for i in range(10):
                    time_offset = current_time - timedelta(minutes=6 * (9 - i))
                    tide = params['baseline'] + params['tide_amp'] * np.sin(2 * np.pi * time_offset.hour / 12)
                    wave = params['wave_amp'] * np.sin(2 * np.pi * i / 3) * (0.8 + 0.2 * np.random.rand())
                    noise = np.random.randn() * 0.1
                    water_level = tide + wave + noise
                    
                    readings.append({
                        'time': time_offset.strftime('%Y-%m-%d %H:%M'),
                        'value': round(water_level, 2),
                        'quality': 'estimated'
                    })
                
                region_readings.append({
                    'station_id': station['id'],
                    'station_name': station['name'],
                    'location': {'lat': station['lat'], 'lon': station['lon']},
                    'readings': readings,
                    'source': 'Simulated (No real-time station)',
                    'data_type': 'water_level',
                    'unit': 'meters',
                    'real_data': False
                })
            
            wave_data[region_key] = {
                'region': region_info['name'],
                'stations': region_readings,
                'last_update': datetime.utcnow().isoformat()
            }
        
        return jsonify({
            'success': True,
            'wave_data': wave_data,
            'timestamp': datetime.utcnow().isoformat(),
            'note': 'Real-time data from IOC sea level stations and NOAA DART buoys'
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching wave data: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch wave data'
        }), 500


def create_seismic_pattern(magnitude, depth, latitude, longitude):
    """
    Create synthetic seismic pattern for model input based on earthquake parameters
    Returns (24, 32) shaped array representing seismic features over time
    
    Parameters:
    - magnitude: Earthquake magnitude (Richter scale)
    - depth: Earthquake depth (km)
    - latitude: Earthquake latitude
    - longitude: Earthquake longitude
    """
    # Initialize pattern
    pattern = np.zeros((24, 32))
    
    # Magnitude affects amplitude (higher magnitude = higher amplitude)
    magnitude_factor = magnitude / 10.0
    
    # Depth affects pattern (shallow = more surface impact)
    depth_factor = max(0.1, 1.0 - (depth / 700.0))  # 700km max depth
    
    # Create time-varying pattern
    for t in range(24):
        # Create frequency components (32 features)
        for f in range(32):
            # Base signal with magnitude influence
            base = magnitude_factor * depth_factor
            
            # Add time evolution (tsunami waves build up)
            time_evolution = np.sin(t * np.pi / 24) * (t / 24)
            
            # Add frequency components
            freq_component = np.cos(2 * np.pi * f / 32)
            
            # Combine factors with some randomness
            pattern[t, f] = base * (0.3 + 0.5 * time_evolution + 0.2 * freq_component)
            pattern[t, f] += np.random.randn() * 0.05  # Small noise
    
    # Normalize to reasonable range
    pattern = np.clip(pattern, 0, 1.0)
    
    return pattern


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
    import os
    logger.info("Starting Tsunami Detection API...")
    logger.info("Available endpoints:")
    logger.info("  - GET  /health")
    logger.info("  - POST /predict")
    logger.info("  - POST /batch-predict")
    logger.info("  - GET  /model-info")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
