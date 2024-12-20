import Spotify as spt
from ytmusicapi import YTMusic
import Youtube as ytb
import json
import Language

#Globals variables
YTM_HEADERS = "headers_auth_ytm.json"
with open(YTM_HEADERS, "r", encoding="utf-8") as arquivo:
    headers = json.load(arquivo)
ytmusic = YTMusic(headers)

#Youtube info
CLIENT_SECRET_FILE = 'ClientYTM.json'
API_NAME = 'youtube'
API_VERSION = 'v3'

#Scopes to youtube API
SCOPES = ["https://www.googleapis.com/auth/youtube"]

#Spotify info
CONFIG_FILE = 'ClientSPT.json'
TOKEN_FILE = 'token.json'

#Load some program configurations
def load_configuration():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return config

config = load_configuration()
sptAuth = {
    'CLIENT_ID': config['CLIENT_ID'],
    'CLIENT_SECRET': config['CLIENT_SECRET'],
    'REDIRECT_URI': config['REDIRECT_URI'],
    'SCOPE': config['SCOPE']
}

#MAIN

close = False
countError = 0
language = 0

while not close:
    language = input('Select your language:\n[1] English [2] Português [3] EXIT\n')

    if language == '1':
        close = True
        text = Language.en()
    elif language == '2':
        close = True
        text = Language.pt()
    elif language == '3':
        exit()
    else:
        countError += 1
        print('Invalid, try again.\nInválido, tente novamente.\n')

    if countError == 3:
        exit()

close = False
countError = 0

while not close:

    opt = input(text[0])

    if opt == '1':
        plt1 = 'Spotify'
        close = True
    elif opt == '2':
        plt1 = 'YouTube'
        close = True
    else:
        countError += 1
        input(text[12])

    if countError == 3:
        exit()

close = False
countError = 0

while not close:

    songs2Add = []

    if plt1 == 'Spotify':
        dic_playlists = spt.get_user_playlists(sptAuth)
        playlist_name = input(text[1])
        print(text[2])
        songs = spt.list_songs(dic_playlists[playlist_name], sptAuth)
        print(text[3])
        ytmusic = ytb.initialize_ytmusic()
        print(text[4])
        for song in songs:
            try:
                songs2Add.append(ytb.search_song(song, ytmusic))
            except:
                print(text[5],song)
        print(text[6])
        playlistYtb = ytb.get_create_playlist(ytmusic, playlist_name)
        print(text[7])
        errors = ytb.update_playlist(ytmusic, songs2Add, playlistYtb)

        if len(errors) > 0:
            print(text[8],errors)

        print(text[9])

    elif plt1 == 'YouTube':
        print('Em desenvolvimento / In developing')

    last = len(text)-1
    close = False if input(text[last]) == '1' else True

