#### EDA #####

# read data
data_B <- read.csv('Data/dataframe_B_features.csv', header = TRUE)
data_B <- data_B[,-2]

tiff('Plots/B_hist_rec.tiff', width = 6, height = 6, units = 'in', res = 300)
hist(data_B$popularity, breaks = 50, main = "Popularity of rec. songs on Spotify", xlab = "Popularity")
dev.off()

# create pairplot

# delete not used columns
dataB_p = data_B[,-c(1,2,4,6,8,11,13,14,16,17,19,20,21)]
tiff('Plots/B_pairplot.tiff', width = 8, height = 8, units = 'in', res = 200)
pairs(dataB_p , upper.panel = panel.smooth, pch = 19, cex = 0.2)
dev.off()

# create boxplot
tiff('Plots/B_boxplot.tiff', width = 8, height = 6, units = 'in', res = 200)
boxplot(popularity~key, data = data_B, names = c("C","C#","D","D#","E","F","F#","G","G#","A","A#","B"), 
        main = "Key",ylab = "popularity")
dev.off()


# linear regression on recommended songs
l_reg <- lm(popularity~valence+loudness+acousticness+instrumentalness+speechiness+
              liveness+mode+tempo+duration+key, data = data_B)
summary(l_reg)

# create the diagnostic plots for the linear regression
tiff('Plots/B_l_reg.tiff', width = 8, height = 6, units = 'in', res = 200)
par(mfrow = c(2,2))
plot(l_reg)
dev.off()

