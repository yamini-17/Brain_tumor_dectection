"""
Advanced Configuration Module for Brain Tumor Detection System
Handles logging, security, and optimization settings.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ============================================================================
# PATHS AND DIRECTORIES
# ============================================================================

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
MODEL_DIR = BASE_DIR / "model"

# Create necessary directories
LOG_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

# ============================================================================
# FLASK CONFIGURATION
# ============================================================================

class Config:
    """Base configuration."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'brain-tumor-detection-key-change-in-production')
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # File upload
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    UPLOAD_FOLDER.mkdir(exist_ok=True)


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging(log_file_name: str = 'app.log') -> logging.Logger:
    """
    Configure logging with both file and console handlers.
    
    Args:
        log_file_name (str): Name of the log file
        
    Returns:
        logging.Logger: Configured logger instance
    """
    
    logger = logging.getLogger('brain_tumor_detection')
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler with rotation
    log_file_path = LOG_DIR / log_file_name
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

class ModelConfig:
    """YOLOv9 Model configuration."""
    
    MODEL_PATH = os.getenv('MODEL_PATH', str(MODEL_DIR / 'yolov9.pt'))
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.5))
    IOU_THRESHOLD = float(os.getenv('IOU_THRESHOLD', 0.45))
    INPUT_SIZE = (640, 640)
    
    # ImageNet normalization (used in preprocessing)
    MEAN = [0.485, 0.456, 0.406]
    STD = [0.229, 0.224, 0.225]
    
    # Device configuration
    USE_GPU = os.getenv('USE_GPU', 'True').lower() == 'true'
    AUTO_DOWNLOAD_MODEL = os.getenv('AUTO_DOWNLOAD_MODEL', 'True').lower() == 'true'


# ============================================================================
# API CONFIGURATION
# ============================================================================

class APIConfig:
    """API and server configuration."""
    
    # Server
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # File upload
    MAX_IMAGE_SIZE = int(os.getenv('MAX_IMAGE_SIZE', 10 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'tif'}
    
    # Request timeouts
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 120))
    
    # Rate limiting (can be enabled with Flask-Limiter)
    ENABLE_RATE_LIMIT = os.getenv('ENABLE_RATE_LIMIT', 'False').lower() == 'true'
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100 per hour')


# ============================================================================
# INFERENCE CONFIGURATION
# ============================================================================

class InferenceConfig:
    """Inference optimization configuration."""
    
    # Batch size (for future batch processing)
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 1))
    
    # Threading
    ENABLE_THREADING = True
    MAX_THREADS = int(os.getenv('MAX_THREADS', 4))
    
    # Caching
    CACHE_PREDICTIONS = os.getenv('CACHE_PREDICTIONS', 'False').lower() == 'true'
    CACHE_SIZE = int(os.getenv('CACHE_SIZE', 100))


# ============================================================================
# GET APPROPRIATE CONFIG
# ============================================================================

def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'production')
    
    if env == 'development':
        return DevelopmentConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return ProductionConfig()
