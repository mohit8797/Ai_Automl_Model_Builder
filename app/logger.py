"""
Logging utilities for AutoML Model Builder
Provides centralized logging configuration and custom loggers
"""

import logging
import logging.handlers
from pathlib import Path
from app.config import Config


class LoggerSetup:
    """Configure application-wide logging"""
    
    _logger_initialized = False
    
    @staticmethod
    def setup():
        """Initialize logging configuration"""
        if LoggerSetup._logger_initialized:
            return
        
        # Ensure log directory exists
        log_dir = Path(Config.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create root logger
        logger = logging.getLogger('automl')
        logger.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(Config.LOG_FORMAT)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            Config.LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler (only in development)
        if Config.DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        LoggerSetup._logger_initialized = True


def get_logger(name):
    """Get a logger instance for a specific module"""
    LoggerSetup.setup()
    return logging.getLogger(f'automl.{name}')


class APIException(Exception):
    """Base exception for API errors"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv


class ValidationException(APIException):
    """Validation error"""
    pass


class ProcessingException(APIException):
    """Processing error during model training"""
    pass


class FileException(APIException):
    """File handling error"""
    pass


def create_error_response(error, status_code=400):
    """Create standardized error response"""
    if isinstance(error, APIException):
        return {
            'status': 'error',
            'message': error.message,
            'details': error.payload
        }, error.status_code
    
    return {
        'status': 'error',
        'message': str(error)
    }, status_code
