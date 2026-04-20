import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    
    # Gemini API configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    # Model configuration
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    
    # Generation configuration
    DEFAULT_IMAGE_SIZE = (1024, 1024)
    MAX_PROMPT_LENGTH = 1000
    
    # File upload configuration (for future features)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size