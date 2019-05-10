import pandas as pd

# concat different dataframes
df1 = pd.read_csv("Data/random_songs1.csv")
df2 = pd.read_csv("Data/random_songs2.csv")
df3 = pd.read_csv("Data/random_songs3.csv")
df4 = pd.read_csv("Data/random_songs4.csv")
df5 = pd.read_csv("Data/random_songs5.csv")
df6 = pd.read_csv("Data/random_songs6.csv")
df7 = pd.read_csv("Data/random_songs7.csv")
df8 = pd.read_csv("Data/random_songs8.csv")
df9 = pd.read_csv("Data/random_songs9.csv")
df10 = pd.read_csv("Data/random_songs10.csv")
df11 = pd.read_csv("Data/random_songs11.csv")

df_com = pd.concat([df1, df2, df3,df4,df5,df6,df7,df8,df9,df10,df11])
df_com.to_csv('Data/random_songs_B.csv')
