import json
import requests
from BenSpotifyInfo import user_id,spotify_token


class CreatePlaylist:
  # a comment that is larger now
  def __init__(self):

    pass

  def get_youtube_client(self):
    pass

  def get_liked_videos(self):
    pass

  def create_playlist(self):
    request_body = json.dumps({
      "name": "Bot Playlist",
      "description": "Made by bot",
      "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type":"application/json",
            "Authorization":"Bearer {}".format(spotify_token)
        }
    )



  def get_spotify_url(self):
    pass

  def add_song_to_playlist(self):
    pass
