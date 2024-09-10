from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
