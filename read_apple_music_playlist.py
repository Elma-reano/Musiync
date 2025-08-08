#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 19:07:28 2025

@author: marianoluna
"""

import pandas as pd
from datetime import datetime as dt
from dateutil import parser

df = pd.read_table('ElmaReanosVoid.txt', sep='\t', encoding= 'utf-16')
# df = pd.read_table('music.txt', sep='\t', encoding= 'utf-16')

def read_file_line(filename: str) -> pd.DataFrame:
    with open(filename, 'r', encoding= 'utf-16') as file:
        for line in file:
            yield line.strip()
        
lista = []
cont = 0
for line in read_file_line('music.txt'):
    lista.append(line.split('\t'))
    cont+=1
    if cont==10000:
        break

df2 = pd.DataFrame(lista)     
df2.columns = (df2.iloc[0].str.lower()
                           .str.strip()
                           .str.replace('á', 'a')
                           .str.replace('é', 'e')
                           .str.replace('í', 'i')
                           .str.replace('ó', 'o')
                           .str.replace('ú', 'u')
                           .str.replace(' ', '_')
               )
df2 = df2[1:]   

df = df[['Nombre', 'Artista', 'Álbum', 'Año']]
df = df.rename(columns= {
    'Nombre': 'name',
    'Artista': 'artist',
    'Álbum': 'album',
    'Año': 'year'
    })

len(df.artist.unique())

df2['ultima_reproduccion'] = df2['ultima_reproduccion'].apply(lambda x: parser.parse(x) if (isinstance(x, str) and x != '') else pd.NaT)



