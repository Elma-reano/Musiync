#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 16:53:49 2025

@author: marianoluna
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Song(Base):
    __tablename__ = 'songs'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(128))
    album = Column(String(128))
    artist_id = Column(Integer, ForeignKey('artists.id'))
    spotify_id = Column(String(64))
    
    artist = relationship('Artist', back_populates= 'songs')
    
    def __repr__(self):
        return f"Song(id={self.id!r}, name={self.name!r}, artist={self.artist!r}, album={self.album!r}, spotify_id={self.spotify_id!r}"
    
    def get_search_query(self):
        return f'''track:{self.name} artist:{self.artist}'''


class Artist(Base):
    __tablename__ = 'artists'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(128))
    spotify_id = Column(String(64))
    
    songs = relationship('Song', back_populates= 'artist')
    
if __name__ == '__main__':
    
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///database.db", echo=True, future=True)
    Base.metadata.create_all(engine)
    
    
    
