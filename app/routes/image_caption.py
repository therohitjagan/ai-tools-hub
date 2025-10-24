from flask import Blueprint, render_template, request, jsonify
from app.models.caption_model import image_captioner
from app.database import db, UsageLog
from werkzeug.utils import secure_filename
import os
import time

image_caption_bp = Blueprint('image_caption', __name__, url_prefix='/image-caption')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_caption_bp.route('/')
def index():
    return render_template('image_caption.html')

@image_caption_bp.route('/api/caption', methods=['POST'])
def generate_caption():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join('app/static/uploads', filename)
        file.save(filepath)
        
        start_time = time.time()
        
        # Generate caption
        detailed = request.form.get('detailed', 'false') == 'true'
        
        if detailed:
            result = image_captioner.generate_detailed_caption(filepath)
            caption = result['detailed']
        else:
            caption = image_captioner.generate_caption(filepath)
        
        processing_time = time.time() - start_time
        
        # Log usage
        log = UsageLog(
            tool_name='image_caption',
            input_text=filename,
            output_text=caption,
            ip_address=request.remote_addr,
            processing_time=processing_time
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'caption': caption,
            'image_url': f'/static/uploads/{filename}',
            'processing_time': round(processing_time, 2)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500