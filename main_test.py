#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:51:49 2025

@author: marianoluna
"""

import pandas as pd

from read_apple_music_playlist import get_my_void_playlist, read_playlist
from models import Artist, Song
from database import (
    get_session,
    add_song_data,
    add_artist_data,
    get_song_database,
    get_artist_database
    )

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
    

def test_song_search():
    
    """
    Cosas por hacer
    Implementar una busqueda sin escribir el artista
    Implementar una busqueda de un titulo alternativo que está escrito en el paréntesis del título?
    
    """
    
    sp: int
    
    def __get_song_info(song: Song) -> dict:
        query = song.get_search_query()
        song_search = sp.search(query)
        if not song_search['tracks']['items']:
            song_search = sp.search(song.name)
        song = song_search['tracks']['items'][0]
        return song
    
    playlist = read_playlist("data/replay2024.txt")
    
    
    def __get_song(row: pd.Series) -> Song:
        return Song(
            name= row['nombre'],
            album= row['album'],
            artist = Artist(name= row['artista'])
            )
    
    song_list = [__get_song(row) for _, row in playlist.iterrows()]
    query = song_list[12].get_search_query()
    song_search = sp.search(query)
    song = song_search['tracks']['items'][0]

    angela = sp.search(song_list[12].get_search_query())
    rene = sp.search(song_list[98].get_search_query())
    edward_garcee = sp.search(song_list[66].get_search_query())
    javo = __get_song_info(song_list[10])
    sandy = __get_song_info(song_list[97])
    cath = __get_song_info(song_list[99])
    castrilla = __get_song_info(song_list[33])
    juanito = __get_song_info(song_list[52])
    jp_morua = __get_song_info(song_list[6])
    juanpi_guzman = __get_song_info(song_list[24])
    ivanner = __get_song_info(song_list[54])
    esteban = __get_song_info(song_list[45])
    erandi = __get_song_info(song_list[1])
    alipi = __get_song_info(song_list[22])
    lezcano = sp.search(song_list[76].name)
    rodo = __get_song_info(song_list[43])
    edy = __get_song_info(song_list[49])
    rendon = __get_song_info(song_list[42])
