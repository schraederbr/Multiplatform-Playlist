# requires SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
# in environment variables.
# SPOTIPY_REDIRECT_URI must be: https://schraederbr.github.io/
# SPOTIPY_REDIRECT_URI

import spotipy
# import json
# import os
# import requests
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read streaming user-read-playback-state user-modify-playback-state user-read-currently-playing " \
        "app-remote-control user-library-modify user-follow-modify playlist-modify-private user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# devices = sp.devices()
#
# songToSearch = input("Enter a song to add to queue: ")
# songToSearch = songToSearch.replace(" ", "+")
# sr = sp.search(songToSearch, 1, 0, "track", None)
# # print(devices)
# for t in sr['tracks']['items']:
#     print(t['uri'])
#     uri = t['uri']
#
# # print(sr)
# ids = []
# # for key in devices:
# #     print(key, ":", devices[key])
#
# for item in devices["devices"]:
#     print(item["id"])
#     ids.append((item["id"], item["is_active"]))
#
# # sp.search
# for device in devices["devices"]:
#     if device["is_active"] and not device["is_restricted"]:
#         # sp.start_playback()
#         sp.add_to_queue(uri)
#         print("'" + t['name'] + "'" + " has been added to your queue")
#
# print('\n')
# topTracks = sp.current_user_top_tracks(5, 0, "long_term")
# print(topTracks)


# this could be cleaned up by making a function for going through the devices
def start_playback():
    device_response = sp.devices()
    for d in device_response["devices"]:
        if device_response["is_active"] and not device_response["is_restricted"]:
            sp.start_playback()


def pause_playback():
    device_response = sp.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            sp.pause_playback()


# Add a check to make sure the user wants to add the song,
# list the name of the song that was found
def add_song_to_queue():
    song_to_search = input("Enter a song to add to queue: ")
    search_response = sp.search(song_to_search, 1, 0, "track", None)
    # print(devices)
    for t in search_response['tracks']['items']:
        print(t['uri'])
        track_uri = t['uri']
    device_response = sp.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            # sp.start_playback()
            sp.add_to_queue(track_uri)
            # + t['artist']
            print("'" + t['name'] + "'" + " by: " + "'" + "'"
                  + " has been added to your queue")


add_song_to_queue()
