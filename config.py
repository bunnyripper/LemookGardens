import os
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")
    
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lemook.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
   
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', SECRET_KEY)
    
   
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    if not ADMIN_USERNAME:
        raise ValueError("ADMIN_USERNAME environment variable is required")
    
    ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH')
    if not ADMIN_PASSWORD_HASH:
        raise ValueError("ADMIN_PASSWORD_HASH environment variable is required")
    
    
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM')
    STAFF_PHONE = os.environ.get('STAFF_PHONE')
    
   
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    STAFF_EMAIL = os.environ.get('STAFF_EMAIL')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', SMTP_USERNAME)
    
    
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        'app', 'static', 'uploads'
    ))
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    
   
    PREFERRED_URL_SCHEME = 'https'
    
    DEBUG=os.environ.get("DEBUG","FALSE") =="True"