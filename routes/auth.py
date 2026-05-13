from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models.user_model import create_user, get_user_by_email, verify_user
from utils.token_handler import generate_token, verify_token
from utils.email_sender import send_verification_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([full_name, email, password, confirm_password]):
            flash("All fields are required.", "error")
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('auth.register'))
        
        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return redirect(url_for('auth.register'))

        existing_user = get_user_by_email(email)
        if existing_user:
            flash("Email already registered.", "error")
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)
        create_user(full_name, email, password_hash)

        token = generate_token(email)
        send_verification_email(current_app.extensions['mail'], email, token)

        flash("Verification email has been sent.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    email = verify_token(token)
    if not email:
        flash("The verification link is invalid or has expired.", "error")
        return redirect(url_for('auth.login'))
    
    user = get_user_by_email(email)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('auth.register'))

    if user.is_verified:
        flash("Account already verified. Please login.", "success")
    else:
        verify_user(email)
        flash("Email verified! Please login.", "success")
        
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)
        if not user:
            flash("Email not found.", "error")
            return redirect(url_for('auth.login'))
            
        if not user.is_verified:
            flash("Please verify your email before logging in.", "error")
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password_hash, password):
            flash("Invalid password.", "error")
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('profile.dashboard'))

    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
