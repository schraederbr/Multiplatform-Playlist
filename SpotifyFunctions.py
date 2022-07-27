# requires SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
# in environment variables.
# SPOTIPY_REDIRECT_URI must be: https://schraederbr.github.io/
# SPOTIPY_REDIRECT_URI

import os
from numpy import indices
import spotipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from json.decoder import JSONDecodeError
import spotipy.util as util
from os.path import exists
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

#Async API requests would speed up things


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
    afters = [None]
    artistIDs = []
    with(open('followed_artists.txt', 'w', encoding="utf-8")) as f:
        followed_artists = SP.current_user_followed_artists(limit=50)
        #f.write(str(followed_artists))
        #print(followed_artists)
        total = followed_artists['artists']['total']
        after = followed_artists['artists']['cursors']['after']
        afters.append(after)
        print(total)
        print(after)
        i = (total // 50)
        print("Total Pages {}".format(i))
        for artist in followed_artists['artists']['items']:
            artistIDs.append(artist['id'])
            #f.write("{}, {}\n".format(str(artist['id']), str(artist['name'])))
            #print(artist['name'])
        while(i > 0):
            followed_artists = SP.current_user_followed_artists(limit=50, after=after)
            #f.write(str(followed_artists))
            after = followed_artists['artists']['cursors']['after']
            afters.append(after)
            for artist in followed_artists['artists']['items']:
                artistIDs.append(artist['id'])
                #f.write("{}, {}\n".format(str(artist['id']), str(artist['name'])))
                #print(artist['name']) 
            i -= 1
        artistIDs = list(set(artistIDs))
        for a in artistIDs:
            f.write("{}\n".format(a))
        f.close()
    return artistIDs

def unfollow_all_artists():
    artistIDs = get_followed_artists()
    i = 0
    while i < len(artistIDs) // 50 + 1:
        ids = artistIDs[i*50:i*50+50]
        print(ids, sep=', ')
        SP.user_unfollow_artists(ids)
        i += 1

def get_user_playlist_IDs():
    allPlaylistIDs = []
    playlist = SP.current_user_playlists(limit=50, offset=0)
    items = playlist['items']
    total = playlist['total']
    offset = 0
    #this causes duplicates if the number of playlists isn't divisible by 50
    #Shouldn't be a problem
    while offset < total:
        playlist = SP.current_user_playlists(limit=50, offset=offset)
        for i in items:
            allPlaylistIDs.append(i['id'])
        offset += 50
        print("offset: {}".format(offset))
    # 
    #print("Total Playlists: {}".format())
    #print(*allPlaylistIDs, sep='\n')
    #print(len(allPlaylistIDs))
    with open('playlist_IDs.txt', 'w', encoding="utf-8") as f:
        for i in allPlaylistIDs:
            f.write("{}\n".format(i))
        f.close()
    print("All Playlist IDs have been written to playlist_IDs.txt")
    return allPlaylistIDs

def get_artists_in_playlists(playlistIDs):
    print("type of playlistIDs{}".format(type(playlistIDs)))
    #I need to deal with people who are featured on songs
    artistIDs = []
    artistNames = []
    if(type(playlistIDs) == str):
        playlistIDs = [playlistIDs]
    for p in playlistIDs:
        p = p.strip()
        playlistDetails = SP.playlist(p)
        print(playlistDetails['name'])
        print("PlaylistIDs: {}".format(p))
        playlistTracks = SP.playlist_tracks(p, limit=100, offset=0)
        #print(playlistTracks)
        total = playlistTracks['total']
        for i in range(total // 100 + 1):
            playlistTracks = SP.playlist_tracks(p, limit=100, offset=i*100)
            for track in playlistTracks['items']:
                for a in track['track']['artists']:
                    artistIDs.append(a['id'])
                    artistNames.append(a['name'])
                # artistIDs.append(track['track']['artists'][0]['id'])
                # artistNames.append(track['track']['artists'][0]['name'])
                    print("ID:{} Name:{}".format(a['id'], a['name']))
        # for i in playlistTracks['items']:
        #     artistIDs.append(i['track']['artists'][0]['id'])
        #     artistNames.append(i['track']['artists'][0]['name'])
        
    artistIDs = list(set(artistIDs)) 
    artistNames = list(set(artistNames))
    print(*artistIDs, sep=', ')
    print(*artistNames, sep=', ')
    print("Total Artists: {}".format(len(artistIDs)))
    return artistIDs

def get_playlist_info(playlistIDs):
    nameIDs = {}
    if(exists("nameIDs.txt")):
        with open('nameIDs.txt', 'r', encoding="utf-8") as f:
            for line in f:
                name, id = line.split(',')
                nameIDs[name] = id
            f.close()
    else:
        if(type(playlistIDs) == list):
            for p in playlistIDs:
                playlistDetails = SP.playlist(p)
                nameIDs[playlistDetails['name']] = p
                #info.append((p, playlistDetails['name']))
        else:
            playlistDetails = SP.playlist(playlistIDs)
            #info.append((p, playlistDetails['name']))
            nameIDs[playlistDetails['name']] = playlistIDs
        print("Playlist Names and IDs:")
        
        with open('nameIDs.txt', 'w', encoding="utf-8") as f:
            for i in nameIDs:
                f.write("{},{}\n".format(i, nameIDs[i]))
            f.close()
    return nameIDs


def search_my_playlists():
    #Cache playlist info or get it to search faster somehow
    returnedPlaylists = []
    playlistInfo = get_playlist_info(get_user_playlist_IDs())
    playlist_to_search = input("Enter playlist term: ")
    i = 0
    for key in playlistInfo:
        if playlist_to_search in key:
            print(i)
            print(key)
            print(playlistInfo[key])
            returnedPlaylists.append(playlistInfo[key])
            i += 1
    selectedIndex = input("Enter indicis: ")
    #print(selectedIndex)
    if(type(selectedIndex) == str):
        selectedIndex = selectedIndex.split(',')
        selectedIndex = selectedIndex[0]
        #print(selectedIndex)
    #print(selectedIndex)
    playlistID = returnedPlaylists[int(selectedIndex)]
    print("PlaylistID: {}".format(playlistID))
    return playlistID
    


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
    # try:
        while True:
            function_to_start = input(
                '1 to play. 2 to pause. 6 next track. 3 to add a song to queue. 4 to print top tracks\n'
                '6 play next track, 7 analyse track, 8 show followed artists\n'
                '9 unfollow all followed artists, 10 get artist IDs from playlist, 11 search playlist\n'
                '12 follow artists in playlist, 5 to sign out. exit to quit\n')
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
                print(get_followed_artists())
            elif function_to_start == '9':
                #Probably need to format the list appropriately or something
                #artists = get_followed_artists()
                #print(artists)
                #SP.user_unfollow_artists(artists)
                unfollow_all_artists()
            elif function_to_start == '10':
                get_playlist_info(get_user_playlist_IDs())
                #get_user_playlist_IDs()
            elif function_to_start == '11':
                search_my_playlists()
            elif function_to_start == '12':
                artists = get_artists_in_playlists(search_my_playlists())
                print(artists)
                print("Len of artists: {}".format(len(artists)))
                for i in range(len(artists) // 50 + 1):
                    SP.user_follow_artists(artists[i * 50:i * 50 + 50])    
            elif function_to_start == '13':
                print(SP.playlist_tracks("45Obyfn0NC7o0e3B3kz2wJ"))
                #SP.user_follow_artists(['06bun5reMRmLxFCbcB6UHW'])
            
            elif function_to_start == 'exit' or function_to_start == 'e' or function_to_start == 'cls':
                #call cls in the shell
                break
            else:
                print('Unrecognized command')
    # except Exception as e:
    #     print(e)
    #     print("\nError occured. Restarting Application\n")
    #     command_line_input()

if __name__ == '__main__':
    command_line_input()
    #example_bar_graph()
    #search_analyze("'I want it that way