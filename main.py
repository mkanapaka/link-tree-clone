import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
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
    return render_template("index.html", social_links=social_links, themes=THEMES, current_theme=current_theme, profile_picture=profile_picture)

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

@app.route("/update_social_links", methods=['POST'])
def update_social_links():
    session['twitter_url'] = request.form.get('twitter_url')
    session['instagram_url'] = request.form.get('instagram_url')
    session['linkedin_url'] = request.form.get('linkedin_url')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
