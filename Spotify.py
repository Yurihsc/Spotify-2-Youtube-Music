import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_user_playlists(sptAuth):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=sptAuth['CLIENT_ID'],
        client_secret=sptAuth['CLIENT_SECRET'],
        redirect_uri=sptAuth['REDIRECT_URI'],
        scope=sptAuth['SCOPE']
    ))

    playlists = sp.current_user_playlists()
    dic_playlists = {}

    for playlist in playlists['items']:
        name = playlist['name']
        playlist_id = playlist['id']
        dic_playlists[name] = playlist_id
        print(f"- {name} ({playlist['tracks']['total']})")

    return dic_playlists

def list_songs(playlist_id, sptAuth):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=sptAuth['CLIENT_ID'],
        client_secret=sptAuth['CLIENT_SECRET'],
        redirect_uri=sptAuth['REDIRECT_URI'],
        scope=sptAuth['SCOPE']
    ))

    results = sp.playlist_items(playlist_id, fields="items(track(name,artists(name))),next")
    songs = []

    while results:
        for item in results['items']:
            track = item['track']
            songName = track['name']
            artists = ", ".join([artist['name'] for artist in track['artists']])
            songs.append(f"{songName} ({artists})")

        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return songs