import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def index():
    # List of social media links
    social_links = [
        {"name": "Twitter", "url": "https://twitter.com/yourusername", "icon": "feather:twitter"},
        {"name": "Instagram", "url": "https://instagram.com/yourusername", "icon": "feather:instagram"},
        {"name": "LinkedIn", "url": "https://linkedin.com/in/yourusername", "icon": "feather:linkedin"},
        {"name": "GitHub", "url": "https://github.com/yourusername", "icon": "feather:github"},
    ]
    return render_template("index.html", social_links=social_links)

@app.route("/upload", methods=['POST'])
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['profile_picture']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile.jpg'))
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
