# requires SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
# in environment variables.
# SPOTIPY_REDIRECT_URI must be: https://schraederbr.github.io/
# SPOTIPY_REDIRECT_URI

import os
import spotipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from json.decoder import JSONDecodeError
import spotipy.util as util
#from dotenv import load_dotenv
# Get the username from terminal
#load_dotenv()
# username = os.getenv("USERNAME")
# client_id = os.getenv("SPOTIPY_CLIENT_ID")
# client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
# redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
username = 'schraederbr'
client_id = "c36c7e2ef6e84235985b72415d66ab13"
client_secret = "a9c49ce1979943648ac35b9d5b39aa16"
redirect_uri = "https://schraederbr.github.io/"


global SCOPE
SCOPE = "ugc-image-upload user-modify-playback-state user-follow-modify user-read-recently-played user-read-playback-position playlist-read-collaborative app-remote-control user-read-playback-state user-read-email streaming user-top-read playlist-modify-public user-library-modify user-follow-read user-read-currently-playing user-library-read playlist-read-private user-read-private playlist-modify-private"
# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, username=username, scope=SCOPE) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, SCOPE) # add scope

# Create our spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)

global SP
SP = spotipy.Spotify(auth=token)

def run_command(spot, funct):
    device_response = spot.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            funct


def start_playback():
    run_command(SP, SP.start_playback())

def pause_playback():
    run_command(SP, SP.pause_playback())

def play_next_track():
    run_command(SP, SP.next_track())

def get_name_artist(response):
    for t in response['tracks']['items']:
        track_uri = t['uri']
    return "'" + t['name'] + "'" + " by: " + "'" + t['artists'][0]['name'] + "'"
# Add a check to make sure the user wants to add the song,
# list the name of the song that was found
def search_song(text):
    song_to_search = input(text)
    search_response = SP.search(song_to_search, 1, 0, "track", None)
    return search_response

def search_song_direct(song_to_search):
    search_response = SP.search(song_to_search, 1, 0, "track", None)
    return search_response

def add_song_to_queue():
    search_response = search_song("Enter a song to add to queue: ")
    track_uri = "spotify:track:7Bmd0vPLxSyFFLH7VXm7T2"
    for t in search_response['tracks']['items']:
        track_uri = t['uri']
    device_response = SP.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            # sp.start_playback()
            SP.add_to_queue(track_uri)
            #use get_name_artist function to shorten this line
            print("'" + t['name'] + "'" + " by: " + "'" + t['artists'][0]['name'] + "'"
                  + " has been added to your queue")

def get_followed_artists():
    artistIDs = []
    with(open('followed_artists.txt', 'w', encoding="utf-8")) as f:
        followed_artists = SP.current_user_followed_artists(limit=50)
        #f.write(str(followed_artists))
        #print(followed_artists)
        total = followed_artists['artists']['total']
        after = followed_artists['artists']['cursors']['after']
        print(total)
        print(after)
        i = (total // 50)
        print("Total Pages {}".format(i))
        for user in followed_artists['artists']['items']:
            artistIDs.append(user['id'])
            f.write("{}, {}\n".format(str(user['id']), str(user['name'])))
            print(user['name'])
        while(i > 0):
            followed_artists = SP.current_user_followed_artists(limit=50, after=after)
            #f.write(str(followed_artists))
            after = followed_artists['artists']['cursors']['after']
            for artist in followed_artists['artists']['items']:
                artistIDs.append(user['id'])
                f.write("{}, {}\n".format(str(artist['id']), str(artist['name'])))
                print(artist['name']) 
            i -= 1
    return artistIDs

def unfollow_artists(artists):
    print(*artists, sep='\n')
    SP.unfollow_artist(artists)


def print_top_tracks():
    how_many = input("How many top tracks to display?")
    if how_many.isdigit():
        top_track_response = SP.current_user_top_tracks(how_many, 0, "long_term")
        for t in top_track_response['items']:
            print("'" + t['name'] + "'" + " by: " + "'" + t['artists'][0]['name'] + "'")
    else:
        print('invalid input')

def search_analyze(query):
    song = search_song_direct(query)
    analyze_song(song)

def analyze_song(song):
    name = get_name_artist(song)
    print(name + " will be analysed")
    track_uri = "spotify:track:7Bmd0vPLxSyFFLH7VXm7T2"
    for t in song['tracks']['items']:
        track_uri = t['uri']
    r = SP.audio_features(track_uri)
    print(r[0])
    plt.figure(figsize=(12, 8), dpi=80)
    plt.title(name + " Audio Features")
    plt.xlabel('Audio Feature', fontweight='bold')
    features = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    values = [r[0]['danceability'], r[0]['energy'], r[0]['speechiness'], r[0]['acousticness'], r[0]['instrumentalness'], r[0]['liveness'], r[0]['valence']]
    plt.bar(features, values)
    #mpld3.show()
    plt.savefig('static/song_features.png')


def sign_out():
    os.remove(f".cache-{username}")

def example_bar_graph():
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = ['C', 'C++', 'Java', 'Python', 'PHP']
    students = [23, 17, 35, 29, 12]
    ax.bar(langs, students)
    plt.show()


def command_line_input():
    try:
        while True:
            function_to_start = input(
                '1 to play. 2 to pause. 6 next track. 3 to add a song to queue. 4 to print top tracks\n'
                '6 play next track, 7 analyse track, 8 show followed users\n'
                '5 to sign out. exit to quit\n')
            if function_to_start == '1':
                start_playback()
            elif function_to_start == '2':
                pause_playback()
            elif function_to_start == '3':
                add_song_to_queue()
            elif function_to_start == '4':
                print_top_tracks()
            elif function_to_start == '5':
                sign_out()
                break
            elif function_to_start == '6':
                play_next_track()
            elif function_to_start == '7':
                analyze_song() #fix this
            elif function_to_start == '8':
                get_followed_artists()
            elif function_to_start == '9':
                unfollow_artists(get_followed_artists)
            elif function_to_start == 'exit' or function_to_start == 'e' or function_to_start == 'cls':
                break
            else:
                print('Unrecognized command')
    except Exception as e:
        print(e)
        print("\nError occured. Restarting Application\n")
        command_line_input()

if __name__ == '__main__':
    command_line_input()
    #example_bar_graph()
    #search_analyze("'I want it that way