from flask import Blueprint, render_template, request, jsonify
from app.models.summarizer_model import summarizer
from app.database import db, UsageLog
import time

summarizer_bp = Blueprint('summarizer', __name__, url_prefix='/summarizer')

@summarizer_bp.route('/')
def index():
    return render_template('summarizer.html')

@summarizer_bp.route('/api/summarize', methods=['POST'])
def summarize_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        max_length = int(data.get('max_length', 150))
        min_length = int(data.get('min_length', 50))
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        if len(text.split()) < 30:
            return jsonify({
                'success': False,
                'error': 'Text is too short. Please provide at least 30 words.'
            }), 400
        
        # Start timing
        start_time = time.time()
        
        # Perform summarization
        summary = summarizer.summarize(text, max_length, min_length)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log usage
        log = UsageLog(
            tool_name='summarizer',
            input_text=text[:500],  # Store first 500 chars
            output_text=summary,
            ip_address=request.remote_addr,
            processing_time=processing_time
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'summary': summary,
            'original_length': len(text.split()),
            'summary_length': len(summary.split()),
            'processing_time': round(processing_time, 2)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500