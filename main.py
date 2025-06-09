import os

from flask import Flask, session, redirect, url_for, request, render_template

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '4dc338481d3348bb8feab99348b5aa03'
client_secret = 'f23dcc594fb043759b5d882b184e4196'
redirect_uri = 'http://127.0.0.1:5000/callback'
scope = 'playlist-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

def check_token():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return True

@app.route('/')
def home():
    if not check_token():
        return None
    return redirect(url_for('get_playlists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))

@app.route('/get_playlists')
def get_playlists():
    if not check_token():
        return None

    playlists_data = sp.current_user_playlists()
    playlists = [{
        'name': pl['name'],
        'id': pl['id'],
        'url': pl['external_urls']['spotify'],
        'image': pl['images'][0]['url'] if pl['images'] else None
    } for pl in playlists_data['items']]

    return render_template('playlists.html', playlists=playlists)

@app.route('/play/<playlist_id>')
def play_playlist(playlist_id):
    if not check_token():
        return None

    devices = sp.devices()
    if not devices['devices']:
        return "No active Spotify device found. Please open Spotify on your device."

    device_id = devices['devices'][0]['id']
    playlist_uri = f'spotify:playlist:{playlist_id}'

    try:
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)
        return f'Started playing playlist: {playlist_id}'
    except Exception as e:
        return f'Erroro starting playback: {str(e)}'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)