#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 19:07:28 2025

@author: marianoluna
"""

import pandas as pd
from datetime import datetime as dt
from dateutil import parser
import os

ELMAREANOSVOID_PATH = 'data/ElmaReanosVoid.txt'

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

def __read_table_by_filelines(path: str,
                              sep: str= ',',
                              max_iterations: int = 10000) -> list[list[str]]:
    def __read_file_line(path: str):
        # TODO autodetect encoding
        with open(path, 'r', encoding= 'utf-16') as file:
            for line in file:
                yield line.strip()
            
                
    table_rows = []
    cont = 0
    for line in __read_file_line(path):
        table_rows.append(line.split(sep))
        cont += 1
        if cont == max_iterations:
            break
        
    return table_rows

def get_my_void_playlist() -> pd.DataFrame:
    
    df = pd.read_table(ELMAREANOSVOID_PATH, sep='\t', encoding= 'utf-16')
    
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
    
    # def __read_file_line(filename: str) -> pd.DataFrame:
    #     with open(filename, 'r', encoding= 'utf-16') as file:
    #         for line in file:
    #             yield line.strip()
            
    # lista = []
    # cont = 0
    # for line in __read_file_line('music.txt'):
    #     lista.append(line.split('\t'))
    #     cont+=1
    #     if cont==10000:
    #         break
    table_list = __read_table_by_filelines('data/music.txt', sep='\t') 
    df2 = pd.DataFrame(table_list)
    
    # df2 = pd.DataFrame(lista)
    df2.columns = clean_columns(df2.iloc[0])
    df2 = df2[1:]   
    
    
    # print(sum(1 for _ in df.artist.unique()))
    
    df2['ultima_reproduccion'] = df2['ultima_reproduccion'].apply(lambda x: parser.parse(x) if (isinstance(x, str) and x != '') else pd.NaT)

def read_playlist(path: str) -> pd.DataFrame:
    if not path:
        raise ValueError("No path was specified")
    elif not os.path.exists(path):
        raise FileNotFoundError(f"File '{path}' was not found")
    #TODO check for file type
    filetype = path.split('.')[-1]
    separator = {
            'csv': ',',
            'tsv': '\t'
        }.get(filetype, '\t')
    # Apple Music playlists tend to separate their values by tab
    
    table_list = __read_table_by_filelines(path, sep= separator)
    df = pd.DataFrame(table_list)
    df.columns = clean_columns(df.iloc[0])
    df = df[1:]
    return df
    
if __name__ == "__main__":
    df1 = get_my_void_playlist()
    df2 = get_all_my_music()
