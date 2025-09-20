#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 16:53:49 2025

@author: marianoluna
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Sequence
from sqlalchemy.orm import declarative_base, relationship

DB_URL = "sqlite:///database.db"
# AIO_DB_URL = "sqlite+aiosqlite:///database.db"

Base = declarative_base()

class Song(Base):
    __tablename__ = 'songs'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    name = Column(String(128))
    album = Column(String(128))
    artist_id = Column(Integer, ForeignKey('artists.id'))
    spotify_id = Column(String(64), unique= True)
    
    artist = relationship('Artist', back_populates= 'songs')
    
    def __repr__(self):
        return f"Song(id={self.id!r}, name={self.name!r}, artist={self.artist!r}, album={self.album!r}, spotify_id={self.spotify_id!r}"
    
    def get_search_query(self):
        return f'''track:{self.name} artist:{self.artist}'''


class Artist(Base):
    __tablename__ = 'artists'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    name = Column(String(128))
    spotify_id = Column(String(64), unique= True)
    
    songs = relationship('Song', back_populates= 'artist')
    

    def __repr__(self):
        return f"<Artist(id={self.id!r}, name={self.name!r}, spotify_id={self.spotify_id!r}>"
    
    def __str__(self):
        return f"{self.name}"
    
def get_engine():
    from sqlalchemy import create_engine
    return create_engine(DB_URL, echo= True, future= True)

# def get_async_engine():
#     from sqlalchemy.ext.asyncio import create_async_engine
#     return create_async_engine(DB_URL, echo=True, future= True)
    
if __name__ == '__main__':
    
    engine = get_engine()
    Base.metadata.create_all(engine)
    
    
    
