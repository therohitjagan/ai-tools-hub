from flask import Flask
from flask_cors import CORS
from config import config
from app.database import db
import os
import logging

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.summarizer import summarizer_bp
    from app.routes.translator import translator_bp
    from app.routes.sentiment import sentiment_bp
    from app.routes.image_caption import image_caption_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(summarizer_bp)
    app.register_blueprint(translator_bp)
    app.register_blueprint(sentiment_bp)
    app.register_blueprint(image_caption_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app