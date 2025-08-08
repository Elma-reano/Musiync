#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 21:41:38 2025
Based on Ian Annase's Spotipy Tutorial
"""

import os
import sys
import spotipy
import json
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

from dotenv import load_dotenv
load_dotenv()

MY_SPOTIFY_USER_ID = os.getenv('MY_SPOTIFY_USER_ID')

# get the username from terminal
username = MY_SPOTIFY_USER_ID
scope = 'user-library-read user-read-private user-read-playback-state user-modify-playback-state'

# Prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)
    
# Create our spotify object
spotify_object = spotipy.Spotify(auth=token)

# Get current device
devices = spotify_object.devices()
device_id = devices['devices'][0]['id']

current_track = spotify_object.current_user_playing_track()
if current_track:
    current_track_artist = current_track['item']['artists'][0]['name']
    current_track_name = track['item']['name']
    print("Currently playing:", artist, '-', track, '\n')

user = spotify_object.current_user()

display_name = user['display_name']
followers = user['followers']['total']

while True:
    
    print()
    print(">>> Welcome to Spotipy,", display_name + "!")
    print(">>> You have" , followers , "followers.")
    print()
    print("0 - Search for an artist")
    print("1- Search for a song")
    print("9 - Exit")
    print()
    
    choice = input("Your choice: ")
    match choice: # noqa
        # Search for the artist
        case "0":
            print()
            search_query = input("Ok. What's their name?: ")
            print()
            
            # get search results
            search_results = spotify_object.search(search_query,
                                                   limit= 2, 
                                                   offset= 0,
                                                   type= 'artist',
                                                   )
                                                   # for some reason, limiting the search to 1 result doesn't give the
                                                   # correct results, so limit 2
                                                   
            # print([a['name'] for a in search_results['artists']['items']])
            artist = search_results['artists']['items'][0]
            print(f"Artist found: {artist['name']}")
            webbrowser.open(artist['images'][0]['url'])
            
            artist_id = artist['id']
            
            track_uris = []
            track_art = []
            z = 0
            
            # Extract album data
            album_results = spotify_object.artist_albums(artist_id)
            album_results = album_results['items']
            
            for item in album_results:
                print("ALBUM", item['name'])
                album_id = item['id']
                album_art = item['images'][0]['url']
                
                # Extract track data
                track_results = spotify_object.album_tracks(album_id)
                track_results = track_results['items']
                
                for track in track_results:
                    print(f"{z}: {track['name']}")
                    track_uris.append(track['uri'])
                    track_art.append(album_art)
                    z += 1
            
            # See album art
            while True:
                song_selection = input("Enter a song number to see the album art (x to exit): ")
                if song_selection.lower() == 'x':
                    break
                track_selection_list = []
                track_selection_list.append(track_uris[int(song_selection)])
                spotify_object.start_playback(device_id, uris=track_selection_list)
                webbrowser.open(track_art[int(song_selection)])
            
        case "1":
            print()
            search_query = input("Ok. Which song?: ")
            print()
            
            # get search_results
            search_results = spotify_object.search(search_query,
                                                   limit= 10,
                                                   offset= 0,
                                                   type= 'track',
                                                   )
            print([(a['name'], a['artists'][0]['name']) for a in search_results['tracks']['items']]) 
            
        # End the program
        case "9":
            print('Bye!')
            break
        
        case _:
            pass
# print(json.dumps(VARIABLE, sort_keys=True, indent= 4))