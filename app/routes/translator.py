from flask import Blueprint, render_template, request, jsonify
from app.models.translator_model import translator
from app.database import db, UsageLog
import time

translator_bp = Blueprint('translator', __name__, url_prefix='/translator')

@translator_bp.route('/')
def index():
    return render_template('translator.html', 
                         languages=translator.get_supported_languages())

@translator_bp.route('/api/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'es')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        start_time = time.time()
        
        # Perform translation
        translation = translator.translate(text, source_lang, target_lang)
        
        processing_time = time.time() - start_time
        
        # Log usage
        log = UsageLog(
            tool_name='translator',
            input_text=f"{source_lang}-{target_lang}: {text[:500]}",
            output_text=translation,
            ip_address=request.remote_addr,
            processing_time=processing_time
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'translation': translation,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'processing_time': round(processing_time, 2)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@translator_bp.route('/api/languages')
def get_languages():
    """Get supported language pairs"""
    return jsonify({
        'success': True,
        'languages': translator.get_supported_languages()
    })