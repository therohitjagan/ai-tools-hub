from flask import Blueprint, render_template, jsonify
from app.database import db, UsageLog
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page with tool selection"""
    return render_template('index.html')

@main_bp.route('/api/stats')
def get_stats():
    """Get usage statistics"""
    try:
        stats = db.session.query(
            UsageLog.tool_name,
            func.count(UsageLog.id).label('count')
        ).group_by(UsageLog.tool_name).all()
        
        total_requests = sum(stat.count for stat in stats)
        
        return jsonify({
            'success': True,
            'total_requests': total_requests,
            'tool_stats': {stat.tool_name: stat.count for stat in stats}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main_bp.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy'}), 200