from flask import jsonify, Blueprint, redirect, url_for, request, render_template, session

from OAuth import check_token, sp, sp_oauth

spotify_bp = Blueprint('spotify', __name__)

# Routes
@spotify_bp.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('spotify.get_playlists'))

@spotify_bp.route('/get_playlists')
def get_playlists():
    if not check_token():
        return check_token()

    playlists_data = sp.current_user_playlists()
    playlists = [{
        'name': pl['name'],
        'id': pl['id'],
        'url': pl['external_urls']['spotify'],
        'image': pl['images'][0]['url'] if pl['images'] else None
    } for pl in playlists_data['items']]

    return render_template('playlists.html', playlists=playlists)

@spotify_bp.route('/play/<playlist_id>')
def play_playlist(playlist_id):
    if not check_token():
        return check_token()

    devices = sp.devices()
    if not devices['devices']:
        return "No active Spotify device found."

    device_id = devices['devices'][0]['id']
    sp.start_playback(device_id=device_id, context_uri=f'spotify:playlist:{playlist_id}')
    return redirect('/current')

@spotify_bp.route('/api/current_playback')
def current_playback():
    if not check_token():
        return jsonify({'error': 'Not authenticated'}), 401

    playback = sp.current_playback()
    if not playback or not playback.get('item'):
        return jsonify({'playing': False})

    item = playback['item']
    return jsonify({
        'playing': playback['is_playing'],
        'track': item['name'],
        'artist': ', '.join([a['name'] for a in item['artists']]),
        'album': item['album']['name'],
        'image': item['album']['images'][0]['url'] if item['album']['images'] else None,
        'progress': playback['progress_ms'],
        'duration': item['duration_ms']
    })

@spotify_bp.route('/current')
def current():
    if not check_token():
        return check_token()
    return render_template('current.html')

@spotify_bp.route('/playback/play', methods=['POST'])
def play():
    if not check_token():
        return jsonify({'error': 'Not authenticated'}), 401
    sp.start_playback()
    return jsonify({'status': 'playing'})

@spotify_bp.route('/playback/pause', methods=['POST'])
def pause():
    if not check_token():
        return jsonify({'error': 'Not authenticated'}), 401
    sp.pause_playback()
    return jsonify({'status': 'paused'})

@spotify_bp.route('/playback/next', methods=['POST'])
def next_track():
    if not check_token():
        return jsonify({'error': 'Not authenticated'}), 401
    sp.next_track()
    return jsonify({'status': 'next'})

@spotify_bp.route('/playback/previous', methods=['POST'])
def previous_track():
    if not check_token():
        return jsonify({'error': 'Not authenticated'}), 401
    sp.previous_track()
    return jsonify({'status': 'previous'})

@spotify_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('spotify.get_playlists'))