from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Config:
    """Base configuration"""
    PROJECT_ROOT = PROJECT_ROOT
    
    # Environment
    ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production-with-strong-secret')
    
    # Upload & File Handling
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 25 * 1024 * 1024))  # 25MB default
    
    # Directories
    UPLOAD_DIR = PROJECT_ROOT / os.getenv('UPLOAD_DIR', 'uploads/datasets')
    MODEL_DIR = PROJECT_ROOT / os.getenv('MODEL_DIR', 'outputs/models')
    INFERENCE_DIR = PROJECT_ROOT / os.getenv('INFERENCE_DIR', 'outputs/inference')
    REPORT_DIR = PROJECT_ROOT / os.getenv('REPORT_DIR', 'outputs/reports')
    LOG_DIR = PROJECT_ROOT / os.getenv('LOG_DIR', 'logs')
    
    # Ensure directories exist
    for directory in [UPLOAD_DIR, MODEL_DIR, INFERENCE_DIR, REPORT_DIR, LOG_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = LOG_DIR / 'automl.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Training Configuration
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 32))
    EPOCHS = int(os.getenv('EPOCHS', 100))
    TEST_SPLIT = float(os.getenv('TEST_SPLIT', 0.2))
    VALIDATION_SPLIT = float(os.getenv('VALIDATION_SPLIT', 0.2))
    
    # Model Configuration
    ENABLE_FEATURE_ENGINEERING = os.getenv('ENABLE_FEATURE_ENGINEERING', 'True').lower() in ('true', '1', 't')
    ENABLE_HYPERPARAMETER_TUNING = os.getenv('ENABLE_HYPERPARAMETER_TUNING', 'False').lower() in ('true', '1', 't')
    ENABLE_CROSS_VALIDATION = os.getenv('ENABLE_CROSS_VALIDATION', 'True').lower() in ('true', '1', 't')
    
    # API Configuration
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 300))  # 5 minutes default
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', 4))
    
    # Database (if needed in future)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    ENV = 'production'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    UPLOAD_DIR = PROJECT_ROOT / 'tests' / 'temp' / 'uploads'
    MODEL_DIR = PROJECT_ROOT / 'tests' / 'temp' / 'models'
    
    # Ensure test directories exist
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}


def get_config():
    """Get appropriate config class based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])