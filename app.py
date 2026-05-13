import os
from flask import Flask
from dotenv import load_dotenv
from config import Config

# Load environment variables from .env file
load_dotenv()
from flask_mail import Mail
from flask_login import LoginManager
from database.db_connection import init_db
from models.user_model import get_user_by_id

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # We need to make sure the folder for profile uploads is ready to go
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Setting up the email system for those verification links
    mail = Mail()
    mail.init_app(app)

    # This part keeps track of who is logged in and handles their session
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    # Let's try to set up the database automatically on startup
    try:
        init_db()
    except Exception as e:
        print(f"Oops! The database couldn't start. Double-check your settings in config.py: {e}")

    # Connecting our authentication and profile pages
    from routes.auth import auth_bp
    from routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
