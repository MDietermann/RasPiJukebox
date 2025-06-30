import os

from flask import Flask, redirect
from API import spotify_bp
from sense_hat import SenseHat

sense = SenseHat()
currently_playing = False

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

app.register_blueprint(spotify_bp)

@app.route('/')
def home():
    return "<h1>Welcome</h1><p><a href='/get_playlists'>View Playlists</a></p>"

if __name__ == '__main__':
    app.run(debug=True)

while True:
    event = sense.stick.wait_for_event()
    
    if event.direction == "right" and event.action == "pressed":
        redirect("/playback/next")
    elif event.direction == "left" and event.action == "pressed":
        redirect("/playback/previous")
    elif event.direction == "up" and event.action == "pressed":
        print("Volume up")
    elif event.direction == "down" and event.action == "pressed":
        print("Volume down")
    elif (event.direction == "middle" and event.action == "pressed"):
        if (currently_playing):
            currently_playing = False
            redirect("/playback/pause")
        else:
            currently_playing = True
            redirect("/playback/pause")
        print(currently_playing)
        