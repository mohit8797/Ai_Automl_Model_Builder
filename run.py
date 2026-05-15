"""
Development server runner for AutoML Model Builder
Use this for local development only. For production, use wsgi.py with Gunicorn.

Run with:
    python run.py
    
Or with Flask CLI:
    FLASK_APP=app flask run
"""

import os
from app import create_app
from app.logger import get_logger

# Get logger
logger = get_logger('run')

# Create Flask app
app = create_app()

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Starting AutoML Model Builder Development Server")
    logger.info("=" * 60)
    logger.info(f"Environment: {app.config['ENV']}")
    logger.info(f"Debug Mode: {app.config['DEBUG']}")
    logger.info(f"Access the application at: http://127.0.0.1:5000")
    logger.info("=" * 60)
    
    # Run Flask development server
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=app.config.get('DEBUG', True),
        use_reloader=True,
        use_debugger=True
    )