import spotipy
import spotipy.util as util
import pandas as pd
import csv
import random
from get_token import get_t

# this program creates a list of random song ids and saves it to csv

# get access to Spotify API
token = get_t()
sp = spotipy.Spotify(auth=token, requests_session=False)

# read the words from a dictionary
words_file = open('Data/words.txt', encoding = 'utf-8')
all_words = words_file.read()
words_file.close()
all_words = all_words.split('\n')

def rword():
    """ picks a random word"""
    word = random.choice(all_words)
    return word

def random_song(n):
    """ returns a list of n ids of random songs"""
    ids = []
    for i in range(n):
        if i%10 == 0:
            print(i)
        while i+1 > len(ids):
            t_name = rword()
            track_id = sp.search(q=' track:' + t_name,
                                 type='track', offset= random.randint(1,1000), limit = 1)
            if len(track_id['tracks']['items'])>0:
                s_id = track_id['tracks']['items'][0]['id']
                ids.append(s_id)
    return ids

# get the random songs
r_song_ids = random_song(12)

# save ids to csv
with open('random_songs.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(r_song_ids)



