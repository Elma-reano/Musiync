#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 19:52:29 2025

@author: marianoluna
"""

import os
import spotipy
import spotipy.util as util
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from spotify_functs import get_playlist_tracks, get_playlists_by_name

MY_SPOTIFY_USER_ID = os.getenv('MY_SPOTIFY_USER_ID')


username = MY_SPOTIFY_USER_ID
scope = 'user-library-read user-read-private playlist-modify-public playlist-modify-private'

# Prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth= token)

names = ['2019 [Géneros Variados]', '2020', '2021', '2022', '2023']
playlists = get_playlists_by_name(username, names, spotify_object= sp)


void = next((p for p in playlists if p['name'] == "ElmaReano's Void"))
void_id = void['id']
void_tracks = sp.user_playlist_tracks(username, playlist_id= void_id)

p2023 = next((p for p in playlists if p['name'] == '2023'))
p2023_tracks = sp.user_playlist_tracks(username, p2023['id'])
p2023_tracks = get_playlist_tracks(p2023_tracks)


# void = [_ for _ in filter(lambda x: x['name'] == "ElmaReanos's Void", playlists)]

# void = sp.user_playlist_create(user= MY_SPOTIFY_USER_ID,
#                             name= "ElmaReano\'s Void",
#                             public= True,
#                             description= "Everything."
#                             )

# TODO agrupar las canciones de la playlist por artista
# los artistas que tengan más de 2 canciones en la playlist, se hace un search del artista
# y se agregan por la lista que te da desde sp.artist_albums()

 