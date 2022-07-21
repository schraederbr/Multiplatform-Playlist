# requires SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
# in environment variables.
# SPOTIPY_REDIRECT_URI must be: https://schraederbr.github.io/
# SPOTIPY_REDIRECT_URI

# DO NOT EDIT THIS, EDIT SpotifyFunctions.py!
import spotipy
# import json
# import os
# import requests
from spotipy.oauth2 import SpotifyOAuth
client_id = "c36c7e2ef6e84235985b72415d66ab13"
client_secret = "a9c49ce1979943648ac35b9d5b39aa16"
redirect_uri = "https://schraederbr.github.io/"
scope = "user-library-read streaming user-read-playback-state user-modify-playback-state user-read-currently-playing " \
        "app-remote-control user-library-modify"

SP = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope ))

results = SP.current_user_saved_tracks()
# print(results)
for idx, item in enumerate(results['items']):
    track = item['track']
    # print(track['uri'])
    # print(idx, track['artists'][0]['name'], " – ", track['name'])

devices = SP.devices()
# print(devices)
songToSearch = input("Enter a song to add to queue: ")
songToSearch = songToSearch.replace(" ", "+")
sr = SP.search(songToSearch, 1, 0, "track", None)
# print(devices)
for t in sr['tracks']['items']:
    print(t['uri'])
    uri = t['uri']

# print(sr)
ids = []
# for key in devices:
#     print(key, ":", devices[key])

for item in devices["devices"]:
    print(item["id"])
    ids.append((item["id"], item["is_active"]))

# sp.search
for device in devices["devices"]:
    if device["is_active"] and not device["is_restricted"]:
        SP.start_playback()
        SP.add_to_queue(uri)
        print("'" + t['name'] + "'" + " has been added to your queue")

print('\n')
topTracks = SP.current_user_top_tracks(5, 0, "long_term")
print(topTracks)

