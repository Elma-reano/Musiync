#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 19:07:28 2025

@author: marianoluna
"""

import pandas as pd
from datetime import datetime as dt
from dateutil import parser

def clean_columns(x: pd.Series or pd.Index) -> pd.Index:
    x = (pd.Series(x).apply(lambda y: '_'.join(y.split()))
                     .str.lower()
                     .str.replace('á', 'a')
                     .str.replace('é', 'e')
                     .str.replace('í', 'i')
                     .str.replace('ó', 'o')
                     .str.replace('ú', 'u')
                     .str.replace('ñ', 'n')
         )
    return pd.Index(x)

def get_my_void_playlist() -> pd.DataFrame:
    
    df = pd.read_table('ElmaReanosVoid.txt', sep='\t', encoding= 'utf-16')
    
    df.columns = clean_columns(df.columns)
    df = df[['nombre', 'artista', 'album', 'ano']]
    df = df.rename(columns= {
        'nombre': 'name',
        'artista': 'artist',
        'album': 'album',
        'ano': 'year'
        })
    df['spotify_id'] = ''
    return df

def get_all_my_music() -> pd.DataFrame:
    
# df = pd.read_table('music.txt', sep='\t', encoding= 'utf-16')
    
    def __read_file_line(filename: str) -> pd.DataFrame:
        with open(filename, 'r', encoding= 'utf-16') as file:
            for line in file:
                yield line.strip()
            
    lista = []
    cont = 0
    for line in __read_file_line('music.txt'):
        lista.append(line.split('\t'))
        cont+=1
        if cont==10000:
            break
    
    df2 = pd.DataFrame(lista)
    df2.columns = clean_columns(df2.iloc[0])
    df2 = df2[1:]   
    
    
    # print(sum(1 for _ in df.artist.unique()))
    
    df2['ultima_reproduccion'] = df2['ultima_reproduccion'].apply(lambda x: parser.parse(x) if (isinstance(x, str) and x != '') else pd.NaT)
    
    
if __name__ == "__main__":
    df1 = get_my_void_playlist()
    df2 = get_all_my_music()
