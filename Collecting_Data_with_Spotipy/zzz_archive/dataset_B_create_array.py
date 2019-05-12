import spotipy
import spotipy.util as util
import pandas as pd
import csv
from get_token import get_t
from random_songs import random_song

with open('Data/random_songs10.csv', "rt", encoding='utf-8') as f:
    reader = csv.reader(f)
    cc = list(reader)

token = get_t()
sp = spotipy.Spotify(auth=token)

audio_feat = []
track_items = []
n = 50
for i in range(int(len(cc[0])/n)):
    rand_s = cc[0][i*n:(i+1)*n]
    audio_feat.append(sp.audio_features(tracks = rand_s))
    track_items.append(sp.tracks(tracks = rand_s))

# apply the procedure of the for loop on the rest of the elements
if not len(cc[0]) % n == 0: 
    rand_s = cc[0][(i+1)*n:]
    audio_feat.append(sp.audio_features(tracks = rand_s))
    track_items.append((sp.tracks(tracks = rand_s)))
               
track_feat = []
for k in track_items:
    for d in k['tracks']:
        track_feat.append({'id': d['id'],'release_date': d['album']['release_date'],
                             'duration' : d['duration_ms'], 'popularity' :  d['popularity'],
                           'track_name' : d['name'], 'artist' : d['artists'][0]['name']})

for entry in track_feat:
    if len(entry['release_date']) == 4:
        entry['release_date'] = entry['release_date'] + '-01-01'
    if len(entry['release_date']) == 7:
        entry['release_date'] = entry['release_date'] + '-01'
    entry['rd_year'] = entry['release_date'][:4]

# flaten the list
audio_feat = [item for sublist in audio_feat for item in sublist]

audio_f = []
track_f = []
for i in range(len(audio_feat)): 
    if audio_feat[i] != None : 
        audio_f.append(audio_feat[i])
        track_f.append(track_feat[i])


df1 = pd.DataFrame(audio_f)
df2 = pd.DataFrame(track_f)

df_merged = pd.merge(df1, df2, on ='id')
cols = [1,14,15,16]
df_merged.drop(df_merged.columns[cols],axis=1,inplace=True)
df_merged.to_csv('Data/random_songs10_sa.csv')
