import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models.user_model import update_profile, update_profile_image, get_user_by_id

profile_bp = Blueprint('profile', __name__)

# If the user is already signed in, we take them to the dashboard, otherwise to the login page
@profile_bp.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile.dashboard'))
    return redirect(url_for('auth.login'))

@profile_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user = get_user_by_id(current_user.id)
    
    # We check which fields are filled to calculate the profile completion percentage
    fields_to_check = [user.full_name, user.phone, user.bio, user.address, user.profile_image]
    filled_fields = sum(1 for field in fields_to_check if field and str(field).strip() != '')
    profile_completion = int((filled_fields / len(fields_to_check)) * 100)
    
    account_status = "Verified" if user.is_verified else "Not Verified"
    
    return render_template('dashboard.html', 
                           user=user, 
                           total_logins=1, 
                           account_status=account_status,
                           profile_completion=profile_completion)

@profile_bp.route('/profile', methods=['GET'])
@login_required
def view_profile():
    user = get_user_by_id(current_user.id)
    return render_template('profile.html', user=user)

@profile_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile_route():
    full_name = request.form.get('full_name')
    phone = request.form.get('phone')
    bio = request.form.get('bio')
    address = request.form.get('address')
    
    if not full_name:
        flash("Full name is required.", "error")
        return redirect(url_for('profile.view_profile'))
        
    # Updating the user's information in the database
    update_profile(current_user.id, full_name, phone, bio, address)
    flash("Profile updated successfully.", "success")
    return redirect(url_for('profile.view_profile'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@profile_bp.route('/upload-photo', methods=['POST'])
@login_required
def upload_photo():
    if 'profile_photo' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('profile.view_profile'))
        
    file = request.files['profile_photo']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('profile.view_profile'))
        
    if file and allowed_file(file.filename):
        # We give the file a random name for organization and extra security
        ext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)
        
        update_profile_image(current_user.id, new_filename)
        flash('Photo uploaded successfully.', 'success')
    else:
        flash('Invalid file format. Allowed: jpg, jpeg, png, webp', 'error')
        
    return redirect(url_for('profile.view_profile'))
