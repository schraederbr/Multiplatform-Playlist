# requires SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
# in environment variables.
# SPOTIPY_REDIRECT_URI must be: https://schraederbr.github.io/

import spotipy
# import json
# import os
# import requests
from spotipy.oauth2 import SpotifyOAuth

client_id = "c36c7e2ef6e84235985b72415d66ab13"
client_secret = "a9c49ce1979943648ac35b9d5b39aa16"

scope = "user-library-read streaming user-read-playback-state user-modify-playback-state user-read-currently-playing " \
        "app-remote-control user-library-modify"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

devices = sp.devices()
# print(devices)

ids = []
for key in devices:
    print(key, ":", devices[key])
for item in devices["devices"]:
    print(item["id"])
    ids.append(item["id"])

sp.start_playback()
