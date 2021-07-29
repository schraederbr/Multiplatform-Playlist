# requires SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
# in environment variables.
# SPOTIPY_REDIRECT_URI must be: https://schraederbr.github.io/
# SPOTIPY_REDIRECT_URI

import spotipy
# import json
# import os
# import requests
from spotipy.oauth2 import SpotifyOAuth

global scope
scope = "user-library-read streaming user-read-playback-state user-modify-playback-state user-read-currently-playing " \
        "app-remote-control user-library-modify user-follow-modify playlist-modify-private user-top-read"
global sp
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def run_command(spot, funct):
    device_response = spot.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            funct


def start_playback():
    run_command(sp, sp.start_playback())

def pause_playback():
    run_command(sp, sp.pause_playback())

def play_next_track():
    run_command(sp, sp.next_track())

def get_name_artist(response):
    for t in response['tracks']['items']:
        track_uri = t['uri']
    return "'" + t['name'] + "'" + " by: " + "'" + t['artists'][0]['name'] + "'"
# Add a check to make sure the user wants to add the song,
# list the name of the song that was found
def search_song(text):
    song_to_search = input(text)
    search_response = sp.search(song_to_search, 1, 0, "track", None)
    return search_response

def add_song_to_queue():
    search_response = search_song("Enter a song to add to queue: ")
    track_uri = "spotify:track:7Bmd0vPLxSyFFLH7VXm7T2"
    for t in search_response['tracks']['items']:
        track_uri = t['uri']
    device_response = sp.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            # sp.start_playback()
            sp.add_to_queue(track_uri)
            #use get_name_artist function to shorten this line
            print("'" + t['name'] + "'" + " by: " + "'" + t['artists'][0]['name'] + "'"
                  + " has been added to your queue")


def print_top_tracks():
    how_many = input("How many top tracks to display?")
    if how_many.isdigit():
        top_track_response = sp.current_user_top_tracks(how_many, 0, "long_term")
        for t in top_track_response['items']:
            print("'" + t['name'] + "'" + " by: " + "'" + t['artists'][0]['name'] + "'")
    else:
        print('invalid input')
        my_main()

def analyze_song():
    song = search_song("Enter song you want to analyse: ")
    print(get_name_artist(song) + " will be analysed")
    #print(song)
    track_uri = "spotify:track:7Bmd0vPLxSyFFLH7VXm7T2"
    for t in song['tracks']['items']:
        track_uri = t['uri']
    print(sp.audio_features(track_uri))


# doesn't work at the moment
# this site might help: https://lambduhh.github.io/2019/09/25/polyjamoury.html
def re_login():
    sc = scope
    sc += " ugc-image-upload"
    global sp
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(show_dialog='true', scope=sc))
    sp.current_user_top_tracks(1, 0, "long_term")

def example_bar_graph():
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = ['C', 'C++', 'Java', 'Python', 'PHP']
    students = [23, 17, 35, 29, 12]
    ax.bar(langs, students)
    plt.show()

def my_main():
    while True:
        function_to_start = input(
            '1 to play. 2 to pause. 6 next track. 3 to add a song to queue. 4 to print top tracks\n'
            '7 analyse track\n'
            '5 to change account. exit to quit\n')
        if function_to_start == '1':
            start_playback()
        elif function_to_start == '2':
            pause_playback()
        elif function_to_start == '3':
            add_song_to_queue()
        elif function_to_start == '4':
            print_top_tracks()
        elif function_to_start == '5':
            re_login()
        elif function_to_start == '6':
            play_next_track()
        elif function_to_start == '7':
            analyze_song()
        elif function_to_start == 'exit':
            break
        else:
            print('Unrecognized command')


my_main()
