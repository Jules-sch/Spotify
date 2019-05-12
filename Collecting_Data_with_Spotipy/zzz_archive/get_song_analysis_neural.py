import spotipy
import spotipy.util as util
import pandas as pd
import csv
from get_token import get_t
import numpy as np

token = get_t()
sp = spotipy.Spotify(auth=token)

def get_sa(ids):
    try:
        audio_feat = sp.audio_analysis(ids )
    
    except:
        return(0)

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
    k = 256
    interval_len = duration/(k)

    # weighted mean of the pitches in each new equidistant interval
    seg_nr = 0
    sum_dur=  sd= 0
    ccc = 0
    pitches_scaled = np.zeros((k,12))


    for i in range(k):
        while sum_dur < (i+1)*interval_len and not seg_nr == (len(segments)):
            if ccc == 0:
                i_seg = segments[seg_nr]
                sd += i_seg['duration']
            if sd <= (i+1)*interval_len and ccc == 0:
                pitches_scaled[i,:] = pitches_scaled[i,:]+(i_seg['duration'])*aa[seg_nr,:]
                seg_nr += 1
                sum_dur = sd           
            elif ccc == 0:
                diff = (i+1)*interval_len - sum_dur
                pitches_scaled[i,:] = pitches_scaled[i,:]+(diff)*aa[seg_nr,:]
                sum_dur += diff
                ccc = 1               
            else:
                if sd-sum_dur <= interval_len:
                    diff = sd-sum_dur
                    pitches_scaled[i,:] = pitches_scaled[i,:]+(diff)*aa[seg_nr,:]
                    sum_dur +=diff
                    ccc = 0
                    seg_nr += 1
                else:
                    pitches_scaled[i,:] = pitches_scaled[i,:]+interval_len*aa[seg_nr,:]
                    sum_dur += interval_len
   
                    
        pitches_scaled[i,:] = pitches_scaled[i,:]/interval_len
         


    # do the same for the timbres
    timbres= [d['timbre'] for d in segments]

    a = np.array(timbres)

    # weighted mean of the timbres in each new equidistant interval
    seg_nr = 0
    sum_dur = sd= 0
    ccc = 0
    timbres_scaled = np.zeros((k,12))
    
    for i in range(k):
        while sum_dur < (i+1)*interval_len and not seg_nr == (len(segments)):
            if ccc == 0:
                i_seg = segments[seg_nr]
                sd += i_seg['duration']
            if sd <= (i+1)*interval_len and ccc == 0:
                timbres_scaled[i,:] = timbres_scaled[i,:]+(i_seg['duration'])*a[seg_nr,:]
                seg_nr += 1
                sum_dur = sd           
            elif ccc == 0:
                diff = (i+1)*interval_len - sum_dur
                timbres_scaled[i,:] = timbres_scaled[i,:]+(diff)*a[seg_nr,:]
                sum_dur = (i+1)*interval_len
                ccc = 1               
            else:
                if sd-sum_dur <= interval_len:
                    diff = sd-sum_dur
                    timbres_scaled[i,:] = timbres_scaled[i,:]+(diff)*a[seg_nr,:]
                    sum_dur +=diff
                    ccc = 0
                    seg_nr += 1
                else:
                    timbres_scaled[i,:] = timbres_scaled[i,:]+interval_len*a[seg_nr,:]
                    sum_dur += interval_len
   
                    
        timbres_scaled[i,:] = timbres_scaled[i,:]/interval_len
         

 
    sa = np.concatenate((pitches_scaled,timbres_scaled), axis = 1)

    return(sa)




