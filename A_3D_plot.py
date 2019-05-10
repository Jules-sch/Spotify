import plotly.plotly as py
import plotly.tools as tls
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties


# read the data
df1 = pd.read_csv("Data/Example_sa.csv")
df1.drop(df1.columns[0], axis=1, inplace = True)


# create 3d plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

df2 = df1[df1['artist']== "Queen"]
ax.scatter(df2['danceability'], df2['energy'], df2['valence'],label = 'Queen - Bohemian Rhapsody', c='orange',
           s = 10, marker='^')
df3 = df1[df1['artist']== "Johnny Cash"]
ax.scatter(df3['danceability'], df3['energy'], df3['valence'], label = 'Johnny Cash - Hurt', c='red',
           s = 10, marker='^')
df3 = df1[df1['artist']== "Daft Punk"]
ax.scatter(df3['danceability'], df3['energy'], df3['valence'], label = 'Daft Punk - Around The World', c='blue',
           s = 10, marker='^')
df3 = df1[df1['artist']== "Coldplay"]
ax.scatter(df3['danceability'], df3['energy'], df3['valence'], label = 'Coldplay - Viva La Vida', c='green',
           s = 10, marker='^')

# add lines
ax.plot([0.414, 0.414], [0.404, 0.404],zs=[0.171,0.23], c= "orange", linewidth = 1)
ax.plot([0.414, 0.48], [0.619, 0.619],zs=[0.416,0.416], c= "green", linewidth = 1)
ax.plot([0.485, 0.485], [0.625, 0.795],zs=[0.416,0.416], c= "green", linewidth = 1)

#ax.set_ylim(1,0)
ax.set_xlabel('danceability')
ax.set_ylabel('energy')
ax.set_zlabel('valence')
plt.legend(loc='upper center', fontsize = "small")


n_f = "Plots/3d_plot.png"
plt.savefig(n_f, dpi = 300)
