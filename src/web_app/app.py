"""
Flask Application Factory
Creates and configures Flask app
"""

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from loguru import logger
import sys

# Configure loguru
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("logs/app.log", rotation="100 MB", retention="30 days", level="DEBUG")

socketio = SocketIO()


def create_app(config_path='config/config.yaml'):
    """
    Create Flask application
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Flask app instance
    """
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'tsunami-warning-system-secret-key-change-in-production'
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS for API access
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize SocketIO for real-time updates
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from .api_routes import api_bp
    from .web_routes import web_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(web_bp, url_prefix='/')
    
    # Health check endpoint - returns 200 status
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Tsunami Early Warning System',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    logger.success("Flask application created successfully")
    
    return app
