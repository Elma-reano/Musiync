#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 17:31:21 2025

@author: marianoluna
"""

import pandas as pd

from models import Song, Artist, get_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

global engine #, async_engine
engine = get_engine()
# async_engine = create_async_engine()

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

# Por el momento no conviene hacer nada en async.
# @contextmanager
# def get_async_session():
#     Session = sessionmaker(async_engine, expire_on_commit= False)
#     session = Session()
#     pass

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
    else:
        print(f"Artist found: {artist!r}")
        if not artist.spotify_id and spotify_id:
            print("Updating artist's spotify_id")
            artist.spotify_id = spotify_id
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
        
def get_song_database(session) -> pd.DataFrame:
    if not session:
        raise Exception("Error. No session was provided")
    
    result = session.execute(
        select(Song.id, Song.name, Song.album, Song.artist_id, Song.spotify_id)
        ).mappings().all()
    df = pd.DataFrame(result)
    df['modified'] = False
    return df

def get_artist_database(session) -> pd.DataFrame:
    if not session:
        raise Exception("Error. No session was provided")
    
    result = session.execute(
        select(Artist.id, Artist.name, Artist.spotify_id)
        ).mappings().all()
    df = pd.DataFrame(result)
    df['modified'] = False
    return df
        
