import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Flask settings
    DEBUG = True
    TESTING = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Database settings
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'resume_analyzer')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Scoring thresholds
    SCORING_THRESHOLDS = {
        'excellent': 80,
        'good': 65,
        'average': 50,
        'poor': 0
    }
