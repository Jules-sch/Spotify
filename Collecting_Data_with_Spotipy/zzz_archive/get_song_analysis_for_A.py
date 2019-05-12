import spotipy
import spotipy.util as util
import pandas as pd
import csv
from get_token import get_t
import numpy as np

token = get_t()
sp = spotipy.Spotify(auth=token)

def get_sa(ids):
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

    # avoid division by 0
    if sum(duration) == 0:
        return 0


    # calculate the weighted means for k intervals of almost equal length
    pitches_s = [d['pitches'] for d in segments]

    aa = np.array(pitches_s)
   
    duration = audio_feat['track']['duration']

    # scale the timbres to k intervals
    k = 36
    interval_len = duration/k

    # weighted mean in each new interval
    seg_nr = 0
    sum_dur = 0
    ccc = 0
    pitches_scaled = np.zeros((k,12))
    for i in range(k):
        seg_dur = 0
        while sum_dur < (i+1)*interval_len and not seg_nr == (len(segments)-1):
            i_seg = segments[seg_nr]
            sum_dur += i_seg['duration']
            pitches_scaled[i,:] = pitches_scaled[i,:]+(i_seg['duration'])*aa[seg_nr,:]
            seg_nr += 1
            seg_dur += i_seg['duration']
        pitches_scaled[i,:] = pitches_scaled[i,:]/seg_dur
    
    lp =  pitches_scaled.tolist()
            
    p_s =  [item for sublist in lp for item in sublist]
     
    pitches_n = ['pitch c','pitch c_s', 'pitch d','pitch d_s','pitch e',
               'pitch f','pitch f_s', 'pitch g','pitch g','pitch a','pitch a_s','pitch b']         
    pitches_name =[]
    for i in range(k):
        for j in range(12):
            pitches_name.append(pitches_n[j]+'-'+str(i+1))

    
    # do the same for the timbres

    timbres= [d['timbre'] for d in segments]

    a = np.array(timbres)

    # weighted mean in each new interval
    seg_nr = 0
    sum_dur = 0
    timbres_scaled = np.zeros((1,k*12))
    for i in range(k):
        seg_dur = 0
        while sum_dur < (i+1)*interval_len and not seg_nr == (len(segments)-1):
            i_seg = segments[seg_nr]
            sum_dur += i_seg['duration']
            timbres_scaled[:,(i*12):((i+1)*12)] =timbres_scaled[:,(i*12):((i+1)*12)]+(i_seg['duration'])*a[seg_nr,:]
            seg_nr += 1
            seg_dur += i_seg['duration']
        timbres_scaled[:,(i*12):((i+1)*12)] =timbres_scaled[:,(i*12):((i+1)*12)]/seg_dur
    
    l =  timbres_scaled.tolist()
            
    t_s =  [item for sublist in l for item in sublist]
            
    timbres_name =[]
    for i in range(k):
        for j in range(12):
            timbres_name.append('timbre scaled'+str(i+1)+'-'+str(j+1))



    keys = pitches_name+timbres_name+['id']
    vals = list(p_s)+list(t_s)+[ids]
    song_ana = dict(zip(keys,vals))
    return(song_ana)

a = get_sa('5i3NO7lO0oe0bdarCIKAXR')


