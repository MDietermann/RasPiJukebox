import os

from flask import Flask

from API import spotify_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

app.register_blueprint(spotify_bp)

@app.route('/')
def home():
    return "<h1>Welcome</h1><p><a href='/get_playlists'>View Playlists</a></p>"

if __name__ == '__main__':
    app.run(debug=True)