import os

from flask import Flask
from API import spotify_bp
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app, resources={r'/*': {
    'origins':
        'http://localhost:8080',
    'allow_headers':
        'Access-Control-Allow-Origin'
}})

app.register_blueprint(spotify_bp)

@app.route('/')
def home():
    return "<h1>Welcome</h1><p><a href='/get_playlists'>View Playlists</a></p>"

if __name__ == '__main__':
    app.run(debug=True)