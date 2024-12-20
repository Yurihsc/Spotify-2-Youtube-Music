import json
from ytmusicapi import YTMusic
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def initialize_ytmusic():
    CLIENT_SECRET_FILE = 'ClientYTM.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'

    SCOPES = ["https://www.googleapis.com/auth/youtube"]

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES
    )

    credentials = flow.run_local_server(port=8080)

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    access_token = credentials.token

    return YTMusic({'Authorization': f'Bearer {access_token}'})


def search_song(song_name, ytmusic):
    return {'name': song_name, 'id':ytmusic.search(song_name, filter="songs")[0]['videoId']}

def get_create_playlist(ytmusic, playlist_name):

    playlists = ytmusic.get_library_playlists()

    playlistsYTM = {playlist['title']: playlist['playlistId'] for playlist in playlists}

    if playlistsYTM.get(playlist_name) is None:
        playlist_id = ytmusic.create_playlist(playlist_name, playlist_name)
    else:
        playlist_id = playlistsYTM[playlist_name]
    return ytmusic.get_playlist(playlist_id)

def update_playlist(ytmusic, songs2Add, playlistYtb):

    errors = []

    for song in songs2Add:
        song_id = song['id']
        add = True
        if len(playlistYtb['tracks']) > 0:
            for track in playlistYtb['tracks']:
                if track['videoId'] == song_id:
                    add = False
                    break
        if add:
            try:
                ytmusic.add_playlist_items(playlistYtb['id'], [song_id])
            except:
                errors.append(song['name'])

    return errors