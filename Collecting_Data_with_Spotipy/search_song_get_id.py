import spotipy
import spotipy.util as util
import csv
from get_token import get_t

# search for a song and then save the results to csv

# get access to api
token = get_t()
sp = spotipy.Spotify(auth=token)

def id(artist,track):
    """ searches for artist name and track name and returns the track id
    If there is no track available it returns 0
    """
    track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track', limit = 1)
    if len(track_id['tracks']['items'])>0:
        s_id = track_id['tracks']['items'][0]['id']
    else:
        s_id = '0'
    return s_id

idx = []
idx.append(id('Queen','Bohemian'))
idx.append(id('Johnny Cash','Hurt'))
idx.append(id('Daft Punk','Around The World'))
idx.append(id('Coldplay','Viva'))

# save as CSV
with open('Data/Example.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(idx)

