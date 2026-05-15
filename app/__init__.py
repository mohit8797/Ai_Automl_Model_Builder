from flask import Flask, jsonify
from app.config import Config, get_config
from app.logger import LoggerSetup, get_logger, APIException, create_error_response

logger = get_logger('app')


def create_app() -> Flask:
    """
    Application factory pattern
    Creates and configures Flask application
    """
    # Initialize logging
    LoggerSetup.setup()
    
    app = Flask(
        __name__,
        template_folder=str(Config.PROJECT_ROOT / "templates"),
        static_folder=str(Config.PROJECT_ROOT / "static"),
        static_url_path="/static",
    )

    # Configuration
    app.config.from_object(get_config())
    
    logger.info(f"Creating Flask app in {app.config['ENV']} environment")
    
    # Register blueprints
    from app.routes.web import web_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    # Error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'environment': app.config['ENV'],
            'version': '1.0.0'
        }), 200
    
    logger.info("Flask app created successfully")
    return app


def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response, status_code = create_error_response(error, error.status_code)
        logger.warning(f"API Exception: {error.message}")
        return jsonify(response), status_code
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        logger.warning(f"Bad request: {str(error)}")
        return jsonify({
            'status': 'error',
            'message': 'Bad request'
        }), 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        logger.warning(f"Not found: {str(error)}")
        return jsonify({
            'status': 'error',
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        logger.error(f"Internal server error: {str(error)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500