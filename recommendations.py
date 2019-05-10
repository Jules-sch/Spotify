import spotipy
import spotipy.util as util
import pandas as pd
import csv
from get_token import get_t
import numpy as np

# get recommendation for a genre and then add it to list if its not yet
# in it and save results to csv

# get access to API
token = get_t()
sp = spotipy.Spotify(auth=token)

n = 50000
k = int(n/50)

song_list = []

# get recommendation and add them if they are not yet in the list
for j in range(k):
    rec = sp.recommendations(seed_genres = ['pop'], limit = 50)
    tracks = rec['tracks']
    
    print(j*50)
    for track in tracks:
        if track['id'] not in song_list:
            song_list.append(track['id'])

# save to csv
with open('indie_songs.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(song_list)



