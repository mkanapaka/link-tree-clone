import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Available themes
THEMES = {
    'default': 'bg-gradient-to-r from-purple-400 via-pink-500 to-red-500',
    'ocean': 'bg-gradient-to-r from-blue-400 via-teal-500 to-green-500',
    'sunset': 'bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500',
    'forest': 'bg-gradient-to-r from-green-400 via-lime-500 to-emerald-500'
}

# Store user profiles
user_profiles = {}

@app.route("/")
def index():
    # Get social media links from session or use default values
    social_links = [
        {"name": "Twitter", "url": session.get('twitter_url', 'https://twitter.com/yourusername'), "icon": "feather:twitter"},
        {"name": "Instagram", "url": session.get('instagram_url', 'https://instagram.com/yourusername'), "icon": "feather:instagram"},
        {"name": "LinkedIn", "url": session.get('linkedin_url', 'https://linkedin.com/in/yourusername'), "icon": "feather:linkedin"},
    ]
    current_theme = session.get('theme', 'default')
    profile_picture = session.get('profile_picture', 'default.jpg')
    edit_mode = session.get('edit_mode', True)  # Default to edit mode
    user_name = session.get('user_name', 'Your Name')  # Get user name from session or use default
    unique_id = session.get('unique_id')
    return render_template("index.html", social_links=social_links, themes=THEMES, current_theme=current_theme, profile_picture=profile_picture, edit_mode=edit_mode, user_name=user_name, unique_id=unique_id)

@app.route("/upload", methods=['POST'])
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['profile_picture']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            session['profile_picture'] = filename
            flash('Profile picture uploaded successfully', 'success')
        except Exception as e:
            app.logger.error(f"Error saving file: {str(e)}")
            flash('Error uploading file', 'error')
        return redirect(url_for('index'))

@app.route("/change_theme", methods=['POST'])
def change_theme():
    theme = request.form.get('theme')
    if theme in THEMES:
        session['theme'] = theme
    return redirect(url_for('index'))

@app.route("/update_profile", methods=['POST'])
def update_profile():
    session['user_name'] = request.form.get('user_name')
    session['twitter_url'] = request.form.get('twitter_url')
    session['instagram_url'] = request.form.get('instagram_url')
    session['linkedin_url'] = request.form.get('linkedin_url')
    flash('Profile updated successfully', 'success')
    return redirect(url_for('index'))

@app.route("/toggle_edit_mode", methods=['POST'])
def toggle_edit_mode():
    session['edit_mode'] = not session.get('edit_mode', True)
    return redirect(url_for('index'))

@app.route("/claim_link", methods=['POST'])
def claim_link():
    unique_id = str(uuid.uuid4())[:8]  # Generate a short unique ID
    session['unique_id'] = unique_id
    
    # Store the current user profile
    user_profiles[unique_id] = {
        'user_name': session.get('user_name', 'Your Name'),
        'profile_picture': session.get('profile_picture', 'default.jpg'),
        'theme': session.get('theme', 'default'),
        'social_links': [
            {"name": "Twitter", "url": session.get('twitter_url', 'https://twitter.com/yourusername'), "icon": "feather:twitter"},
            {"name": "Instagram", "url": session.get('instagram_url', 'https://instagram.com/yourusername'), "icon": "feather:instagram"},
            {"name": "LinkedIn", "url": session.get('linkedin_url', 'https://linkedin.com/in/yourusername'), "icon": "feather:linkedin"},
        ]
    }
    
    flash(f'Your unique link has been created: {request.host_url}u/{unique_id}', 'success')
    return redirect(url_for('index'))

@app.route("/u/<unique_id>")
def shared_profile(unique_id):
    profile = user_profiles.get(unique_id)
    if profile:
        return render_template("shared_profile.html", profile=profile, themes=THEMES)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
