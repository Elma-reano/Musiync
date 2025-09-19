#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 17:31:21 2025

@author: marianoluna
"""

import pandas as pd

from models import Song, Artist, get_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

global engine
engine = get_engine()
Session = sessionmaker(engine, expire_on_commit= False)

from contextlib import contextmanager

@contextmanager
def get_session():
    Session = sessionmaker(engine, expire_on_commit= False)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def add_artist_data(session,
                    artist_name: str,
                    spotify_id: str = None):
    if not session:
        raise Exception("Error. No session was provided")
    
    artist = session.execute(
        select(Artist)
        .where(Artist.name == artist_name)
        ).scalar_one_or_none()
    
    if not artist:
        new_artist = Artist(name= artist_name, spotify_id= spotify_id)
        session.add(new_artist)
        # session.commit()
    else:
        print(f"Artist found: {artist!r}")
        if not artist.spotify_id and spotify_id:
            print("Updating artist's spotify_id")
            artist.spotify_id = spotify_id
            # session.commit()        
    return
            

def add_song_data(session,
                  song_name: str,
                  album_name: str,
                  artist: Artist,
                  spotify_id: str = None):
    if not session:
        raise Exception("Error. No session was provided")
    song = session.execute(
        select(Song)
        .where(Song.name == song_name and 
               Song.album == album_name and
               Song.artist == artist)
        ).scalar_one_or_none()
    
    if not song:
        new_song = Song(name= song_name,
                        album= album_name,
                        artist= Artist,
                        spotify_id= spotify_id)
        session.add(new_song)
        # session.commit()
        
def get_song_database(session) -> pd.DataFrame:
    if not session:
        raise Exception("Error. No session was provided")
    
    result = session.execute(
        select(Song.id, Song.name, Song.album, Song.artist_id)
        ).mappings().all()
        