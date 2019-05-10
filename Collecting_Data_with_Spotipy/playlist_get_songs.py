import spotipy
import spotipy.util as util
import pandas as pd
import csv
from get_token import get_t

# this program creates a dataframe which contains the information of tracks
# from a given playlist and saves to csv.
# to use it for another playlist just change the user and playlist_id (ln 33)

song = []
audio_feat= []

# function takes the values from a playlist object
# and adds the track infos to the list song and audio_feat
def create_lists(u_p):
    result = []
    track_items = u_p['items']
    for track in track_items:
        result.append(track['track']['id'])
    for d in track_items:
        song.append({'id': d['track']['id'],'release_date': d['track']['album']['release_date'],
                         'duration' : d['track']['duration_ms'], 'popularity' :  d['track']['popularity'],
                       'track_name' : d['track']['name'], 'artist' : d['track']['artists'][0]['name']})
    audio_feat.extend(sp.audio_features(tracks =result))

# get access 
token = get_t()
sp = spotipy.Spotify(auth=token)


# get information from a playlist
u_play = sp.user_playlist('9gSE1TQGQNmDyMnUulEM9A', playlist_id= '5GEf0fJs9xBPr5R4jEQjtw', fields='tracks,next')

# if the playlist is too large, next is used
tracks = u_play['tracks']
create_lists(tracks)
while tracks['next']:
    tracks = sp.next(tracks)
    create_lists(tracks)


for entry in song:
    if len(entry['release_date']) == 4:
        entry['release_date'] = entry['release_date'] + '-01-01'
    if len(entry['release_date']) == 7:
        entry['release_date'] = entry['release_date'] + '-01'
    entry['rd_year'] = entry['release_date'][:4]

df1 = pd.DataFrame(audio_feat)
df2 = pd.DataFrame(song)

df_merged = pd.merge(df1, df2, on ='id')
cols = [1,14,15,16]
df_merged.drop(df_merged.columns[cols],axis=1,inplace=True)
df_merged.to_csv('Data/chart_songs.csv')


