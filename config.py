import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    
    # Database connection
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:040802@localhost:5432/Login_Page')
    
    # Email settings 
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'vaibhav.sv007@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'qvyetuycsrgxqbjc')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'Demo App')

    # Settings for handling profile photo uploads (Max 2MB and specific formats)
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
