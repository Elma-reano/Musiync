#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:51:49 2025

@author: marianoluna
"""

import pandas as pd

from read_apple_music_playlist import get_my_void_playlist
from database import (
    get_session,
    add_song_data,
    add_artist_data,
    get_song_database,
    get_artist_database
    )
from models import Artist, Song

def update_database_from_apple_music():
    
    playlist_df = get_my_void_playlist()
    
    with get_session() as session:
        song_df = get_song_database(session)
        artist_df = get_artist_database(session)
        
    new_songs = playlist_df[
            ~(playlist_df['name'] + playlist_df['artist']).isin(song_df['name'] + song_df['artist'])
        ]
    new_artists = playlist_df[
            ~playlist_df['artist'].isin(artist_df['name'])
        ]
    
    with get_session() as session:
        for row in new_songs.iterrows():
            session.add(Song(
                name= row['name'],
                artist= row['artist']
                ))
    
