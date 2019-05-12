import pandas as pd
import numpy as np
from get_song_analysis_for_B import get_sa

data = pd.read_csv('Data/dataframe_A.csv',sep = ',',encoding='utf-8')
d_id = data['id']
l_ids = list(d_id)

song_ana = np.zeros((len(l_ids),256,24))
sa_id = []

j = 0
for i, ids in enumerate(l_ids):
    sa = get_sa(ids)
    if not type(sa) == 'int':
        song_ana[j,:,:] = sa
        sa_id.append(ids)
        j += 1
    else:
        song_ana = song_ana[0:-1,:,:]

    if i % 50 ==0:
        print(i)
        
np.save('Data/rs_A.npy', song_ana)    # .npy extension is added if not given
np.save('Data/rs_A_ids.npy', sa_id) 
# d = np.load('test3.npy')
