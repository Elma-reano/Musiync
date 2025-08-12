#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:56:05 2025

@author: marianoluna
"""

import os
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
load_dotenv()

# MY_SPOTIFY_USER_ID = os.getenv('MY_SPOTIFY_USER_ID')

# username = MY_SPOTIFY_USER_ID
# scope = 'user-library-read user-read-private playlist-modify-public playlist-modify-private'

def get_spotify_object(username: str, scope: str or list) -> str:
    
    if isinstance(scope, list):
        scope = ' '.join(scope)

    # Prompt for user permission
    try:
        token = util.prompt_for_user_token(username, scope)
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)

    spotify_object = spotipy.Spotify(auth= token)
    
    return spotify_object

def get_playlists_by_name(username: str,
                          names: list[str], 
                          spotify_object: spotipy.client.Spotify
                          ) -> list[dict]:
    user_playlists = spotify_object.user_playlists(username, limit= 100)
    playlist_list = user_playlists['items']
    
    while True:
        if user_playlists['next']:
            user_playlists = spotify_object.next(user_playlists['next'])
            playlist_list += user_playlists['items']
            continue
        break
    
    playlist_list = list(filter(lambda p: p['name'] in names, playlist_list))
    return playlist_list

def get_playlist_tracks(playlist: dict) -> list[dict]:
    if playlist:
        return [{
                'name': x['track']['name'],
                'id': x['track']['id'],
                'album': x['track']['album']['name'],
                'artist': x['track']['artists'][0]['name'],
                'artist_id': x['track']['artists'][0]['id']
            } for x in playlist['items']
            ]
    else:
        return None

# playlists = sp.user_playlists(MY_SPOTIFY_USER_ID)
# playlists = playlists['items']
