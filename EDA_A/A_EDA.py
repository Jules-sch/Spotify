import plotly.plotly as py
import plotly.tools as tls
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

## read the data
df1 = pd.read_csv("Data/dataframe_A.csv")
df1.drop(df1.columns[0], axis=1, inplace = True)

### create histograms #####

# cols to create histograms
l_col = ['danceability', 'energy','instrumentalness', 'key',
         'liveness', 'loudness',
         'speechiness', 'tempo',  'valence']

for col in l_col:

    fig = plt.figure()

    # split the data
    random_s = df1[df1['chart_random'] == 0]
    chart_s = df1[df1['chart_random'] == 1]

    num_bins = 50

    # the histogram of the data - for column
    plt.hist(random_s[col], num_bins, alpha = 0.95,facecolor='#333C3C',
             label = 'Random', density = True)
    plt.hist(chart_s[col], num_bins, alpha = 0.7, facecolor='#81B69D',
             label = 'Chart', density = True)

    plt.xlabel(col)
    plt.ylabel('Density')
    plt.legend(loc='upper left')
    plt.title(col)

    n_f = "Plots/hist_"+col + ".png"
    plt.savefig(n_f, dpi = 300)


#### mode #####
col = 'mode'
fig = plt.figure()

labels = ['Minor', 'Major']
x = [0,1]
# split the data
random_s = df1[df1['chart_random'] == 0]
chart_s = df1[df1['chart_random'] == 1]

num_bins = 50

# the histogram of the data - for column
plt.hist(random_s[col], num_bins, alpha = 0.95,facecolor='#333C3C',
         label = 'Random', density = True)
plt.hist(chart_s[col], num_bins, alpha = 0.7, facecolor='#81B69D',
         label = 'Chart', density = True)

plt.xlabel(col)
plt.ylabel('Density')
plt.legend(loc='upper left')
plt.title(col)
plt.xticks(x,labels)

n_f = "Plots/hist_"+col + ".png"
plt.savefig(n_f, dpi = 300)


