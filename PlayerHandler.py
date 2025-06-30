from OAuth import check_token, sp
from sense_hat import SenseHat

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