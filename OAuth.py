from flask import redirect, session, url_for, request
from spotipy import FlaskSessionCacheHandler, SpotifyOAuth, Spotify

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

def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))