#### EDA  on random songs #####

data_B <- read.csv('Data/dataframe_b2_features.csv', header = TRUE)
tiff('Plots/B_hist_random.tiff', width = 6, height = 6, units = 'in', res = 300)
hist(data_B2$popularity, breaks = 50, main = "Popularity of random songs on Spotify", xlab = "Popularity")
dev.off()


# create pairplot
dataB_p = data_B[,-c(1,2,5,7,9,12,15,17,20,21,22)]
tiff('Plots/B_pairplot.tiff', width = 8, height = 8, units = 'in', res = 200)
pairs(dataB_p , upper.panel = panel.smooth, pch = 19, cex = 0.3)
dev.off()

# create boxplot
tiff('Plots/B_boxplot.tiff', width = 8, height = 6, units = 'in', res = 200)
boxplot(popularity~key, data = data_B, names = c("C","C#","D","D#","E","F","F#","G","G#","A","A#","B"), 
        main = "Key",ylab = "popularity")
dev.off()


# linear regression 
l_reg <- lm(popularity~acousticness+danceability+energy+instrumentalness+loudness+liveness+
              speechiness+valence, data = data_B)
summary(l_reg)


### pca #####
dataB_pca = data_B[,-c(1,2,5,7,17,21,22)]
pca <- prcomp(dataB_pca,scale = T, center = T)
screeplot(pca)

summary(data_B)

