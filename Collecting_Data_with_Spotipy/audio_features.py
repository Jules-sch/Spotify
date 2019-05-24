import spotipy
import spotipy.util as util
import pandas as pd
import csv
from get_token import get_t

# this program creates a dataframe with audio features for a list of song ids

token = get_t()
sp = spotipy.Spotify(auth=token)


def get_song_f(s_list):
    """returns the audio features and track features for a list of songs"""
    
    audio_feat = []
    track_items = []

    # it only returns the features for 50 songs. It is only possible to apply
    # this request for 50 elements. Spilt the list:
    n = 50
    for i in range(int(len(s_list)/n)):
        rand_s = s_list[i*n:(i+1)*n]
        audio_feat.append(sp.audio_features(tracks = rand_s))
        track_items.append(sp.tracks(tracks = rand_s))

    # apply the procedure of the for loop on the rest of the elements
    if not len(s_list) % n == 0:
        rand_s = s_list[((len(s_list)//n)*n):]
        audio_feat.append(sp.audio_features(tracks = rand_s))
        track_items.append(sp.tracks(tracks = rand_s))
    
        
    # get the track features                  
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
    return(audio_f,track_f)


# read list of ids
with open('Data/Example.csv', "rt", encoding='utf-8') as f:
    reader = csv.reader(f)
    cc = list(reader)

song_list = cc[0]

audio_f, track_f = get_song_f(song_list)
df1 = pd.DataFrame(audio_f)
df2 = pd.DataFrame(track_f)

# save to csv
df_merged = pd.merge(df1, df2, on ='id')
cols = [1,14,15,16]
df_merged.drop(df_merged.columns[cols],axis=1,inplace=True)
df_merged.to_csv('Data/Example_sa.csv')

