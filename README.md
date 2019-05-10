# Spotify Data Analysis

The main goal of this project is to find out what properties a song needs to have to be popular. I will try to approach this question from two different angles and work with the two datasets:

Dataset A: UK Number 1 vs. random songs (ca. 2,600 observations of 16 variables)
It contains data from approximately 1,300 songs that were Number 1 songs in the UK (from playlist “Every Official UK Number 1 Ever” from user “Official Charts”) and 1,300 random songs.

For Dataset A the aim is to detect the main differences between the two groups.

Dataset B: 10,000 recommended songs (ca. 10,000 observations of ca. 130 variables)
Dataset B2: 10,000 random songs (ca. 10,000 observations of ca. 130 variables)

# Collecting data with Spotipy

With get_token.py it is possible to get access the Spotify API. Then if the access established then one use: 

random_songs.py to get randon song ids
playlist_get_songs.py to collect track infos from a user playlist
recommendations.py to get recommendations for a given genre
search_song_get_id.py to get and id for track name and artist name
song_analysis.py get summarized values of the song analysis for song ids
song_features.py get song features for song ids

