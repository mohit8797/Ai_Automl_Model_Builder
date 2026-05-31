import os
from app import create_app
from app.logger import get_logger

logger = get_logger('run')

app = create_app()

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Starting AutoML Model Builder Development Server")
    logger.info("=" * 60)

    port = int(os.environ.get("PORT", 5000))

    logger.info(f"Access the application at: http://0.0.0.0:{port}")
    logger.info("=" * 60)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=app.config.get('DEBUG', True)
    )
