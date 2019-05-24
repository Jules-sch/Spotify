import spotipy
import spotipy.util as util
import pandas as pd
import csv
from get_token import get_t
import numpy as np

# this program returns for a given dataframe with audio features the summarized values
# of the audio analysis like mean of pitches, cor of pitches, covariances of pitches
# mean of timbres, var of timbres

# get access
token = get_t()
sp = spotipy.Spotify(auth=token)

def get_sa(ids):
    """ for a song id (ids) it returns the summarized values of the song analysis"""
    audio_feat = sp.audio_analysis(ids )

    if audio_feat == None:
        return 0

    # create liste of segments and sections
    segments = audio_feat['segments']
    sections = audio_feat['sections']

    card_sections = len(sections)

    key = audio_feat['track']['key']
    keys_s = [d['key'] for d in sections]
    duration = [d['duration'] for d in sections]

    lmax = [d['loudness_max'] for d in segments]
    pitches_s = [d['pitches'] for d in segments]

    # create mean vector of means
    aa = np.array(pitches_s)

    # shift the values that the root (fundamental tone) is at the first position
    # a = numpy.zeros(aa.shape)
    # a[:,:(12-key)] = aa[:,key:]
    # a[:,(12-key):] = aa[:,:key]

    a = aa
      
    pitches_mean = (np.mean(a, axis=0))
    pitches_var = (np.var(a, axis=0))
    # create correlation matrix
    corr = np.corrcoef(np.transpose(a))

    pitches_cor = []
    pitches_c_name =[]
    for i in range(11):
        pitches_cor = pitches_cor + list(corr[i,i+1:12])
        for j in range(i+1,12):
            pitches_c_name.append('pitch corr '+str(i+1)+'-'+str(j+1))
            
    pitches = ['pitch c','pitch c_s', 'pitch d','pitch d_s','pitch e',
               'pitch f','pitch f_s', 'pitch g','pitch g','pitch a','pitch a_s','pitch b']
    pitches_v = ['p var c','p var c_s', 'p var d','p var d_s','p var e',
               'p var f','p var f_s', 'p var g','p var g','p var a','p var a_s','p var b']

            
    # Do the same for the timbres

    timbres= [d['timbre'] for d in segments]

    a = np.array(timbres)

    timbres_mean = (np.mean(a, axis=0))
    timbres_var = (np.var(a, axis=0))

    timbres_m_names = []
    timbres_v_names =[]

    for i in range(12):
        timbres_m_names.append('timbre_mean_' + str(i+1))
        timbres_v_names.append('timbre_var_' + str(i+1))
        
    keys = pitches+pitches_v+pitches_c_name+timbres_m_names+timbres_v_names+['id']
    vals = list(pitches_mean)+list(pitches_var)+list(pitches_cor)+list(timbres_mean)+list(timbres_var)+[ids]
    song_ana = dict(zip(keys,vals))
    return(song_ana)

# open dataframe 
df1 = pd.read_csv("Data/dataframe_B2.csv")

# get ids
idx = list(df1['id'])

audio_ana = []
for i,track in enumerate(idx):
    s_a = get_sa(track)
    audio_ana.append(s_a)
    if i % 100 == 0:
        print(i)

### save to csv ###

# omit the rows, for which there is no audio analysis available
audio_ana2 = [item for item in audio_ana if type(item) == dict]
df2 = pd.DataFrame(audio_ana2)

df_merged = pd.merge(df1, df2, on ='id')
df_merged.to_csv('Data/dataframe_B2_sa2.csv')


