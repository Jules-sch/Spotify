#### load Data ####
dataA <- read.csv('Data/dataframe_A.csv', header = TRUE)
dataA <- dataA[,-4]
dataA$chart_random_f[dataA$chart_random==0] <- "random"
dataA$chart_random_f[dataA$chart_random==1] <- "chart"
dataA$chart_random_f <- as.factor(dataA$chart_random_f)

######### EDA ###########

library(vcd)
boxplot(loudness~chart_random_f, data = dataA)

# calculate odd-ratio
cr_mode <- structable(chart_random_f~mode, data=dataA)
cr_mode <- cr_mode[c(2,1),]
a <- as.numeric(cr_mode[1,1]*cr_mode[2,2]/(cr_mode[1,2]*cr_mode[2,1]))
fisher.test(as.table(cr_mode))


### pca ###
dataA_pc <- dataA[,-c(1,5,15,17,18,19,20,21,22)]
pca <- prcomp(dataA_pc,scale = T, center = T)
tiff('Plots/A_biplot1.tiff', width = 6, height = 6, units = 'in', res = 300)
biplot(pca, xlabs=rep("", 2635),cex = 0.5, col = "black", xlim = c(-.04,0.04), ylim = c(-0.022,0.019))
dev.off()
tiff('Plots/A_screeplot.tiff', width = 6, height = 6, units = 'in', res = 300)
screeplot(pca)
dev.off()
var <- pca$sdev^2
cumsum(var)/sum(var)

# create 2nd bi plot
library(factoextra)
tiff('Plots/A_biplot2.tiff', width = 8, height = 8, units = 'in', res = 300)
plot(fviz_pca_biplot(pca, label="var",col.var="black", ylim = c(-5,5),
                     habillage=as.factor(dataA$chart_random_f),palette = c("#81B69D", "black")) + ggtitle("") +
       theme(text = element_text(size = 14), 
             panel.background = element_blank(), 
             panel.grid.major = element_blank(), 
             panel.grid.minor = element_blank(), 
             axis.line = element_line(colour = "black")
       ))
dev.off()

### pairplots and correlations ###
dataA_p = dataA_pc[,-c(5,8,11)]
dataA_p$popularity = dataA$popularity
tiff('Plots/A_pairplot.tiff', width = 8, height = 8, units = 'in', res = 200)
pairs(dataA_p , upper.panel = panel.smooth, pch = 19, cex = 0.3)
dev.off()

library(corrplot)
jpeg('Plots/A_corrplot.tiff', width = 8, height = 8, units = 'in', res = 300)
corrplot(cor(dataA_p), tl.col="black", method="color", addCoef.col = "black",order = "AOE",number.cex=0.6)
dev.off()