#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 17:31:21 2025

@author: marianoluna
"""

import pandas as pd

from models import Song, Artist, get_engine
from sqlalchemy.orm import Session
from sqlalchemy import select, update

engine = get_engine()

def add_artist_data(artist_name: str,
                    spotify_id: str = None):
    with Session(engine) as session:
        artist = session.execute(
            select(Artist)
            .where(Artist.name == artist_name)
            ).scalar_one_or_none()
        
        if not artist:
            new_artist = Artist(name= artist_name, spotify_id= spotify_id)
            session.add(new_artist)
            session.commit()
        else:
            print(f"Artist found: {artist!r}")
            if not artist.spotify_id and spotify_id:
                print("Updating artist's spotify_id")
                artist.spotify_id = spotify_id
                session.commit()        
    return
            