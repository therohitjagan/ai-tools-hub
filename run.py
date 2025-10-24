#!/usr/bin/env python3
"""
Main entry point for the AI Tools Hub application
"""
import os
from app import create_app

# Get configuration from environment or default to development
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = config_name == 'development'
    
    print(f"""
    ╔═══════════════════════════════════════╗
    ║     AI Tools Hub Starting...          ║
    ║                                       ║
    ║  Environment: {config_name:<20}  ║
    ║  Port: {port:<28}  ║
    ║  Debug: {str(debug):<27}  ║
    ╚═══════════════════════════════════════╝
    """)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )