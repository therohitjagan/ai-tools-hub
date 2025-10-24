from flask import Blueprint, render_template, request, jsonify
from app.models.sentiment_model import sentiment_analyzer
from app.database import db, UsageLog
import time

sentiment_bp = Blueprint('sentiment', __name__, url_prefix='/sentiment')

@sentiment_bp.route('/')
def index():
    return render_template('sentiment.html')

@sentiment_bp.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        start_time = time.time()
        
        # Perform sentiment analysis
        result = sentiment_analyzer.analyze(text)
        
        processing_time = time.time() - start_time
        
        # Log usage
        log = UsageLog(
            tool_name='sentiment',
            input_text=text[:500],
            output_text=str(result),
            ip_address=request.remote_addr,
            processing_time=processing_time
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'result': result,
            'processing_time': round(processing_time, 2)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500