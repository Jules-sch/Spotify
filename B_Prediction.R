#### find the best predictor #####

#load the data
data_B <- read.csv('Data/dataframe_B_features.csv', header = TRUE)
data_B <- data_B[,-2]
set.seed(145)

#### lin model only with mean #####

# Randomly shuffle the data
data_B2<-data_B[sample(nrow(data_B)),-c(1,4,6,16,20,21)]

# Create 10 equally size folds
folds <- cut(seq(1,nrow(data_B2)),breaks=10,labels=FALSE)

# Perform 10 fold cross validation
err_lreg_mae <- err_lreg_mse <- numeric(10)

for(i in 1:10){
  # Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B2[testIndexes, ]
  trainData <- data_B2[-testIndexes, ]
  
  # Lin reg
  l_reg <- lm(popularity~1, data= trainData)
  pred_ch_r <- predict.glm(l_reg, testData[,-14])
  err_lreg_mae[i] <- sum(abs(pred_ch_r-testData$popularity))/length(pred_ch_r)
  err_lreg_mse[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
}

# ma error of the mean
sum(err_lreg_mae)/10

# ms error of the mean
sum(err_lreg_mse)/10



#### linear regression with audio features ######

# Randomly shuffle the data
data_B2<-data_B[sample(nrow(data_B)),-c(1,4,6,16,20,21)]

# Create 10 equally size folds
folds <- cut(seq(1,nrow(data_B2)),breaks=10,labels=FALSE)

# Perform 10 fold cross validation
err_lreg_mae <- err_lreg_mse <- numeric(10)
for(i in 1:10){
  # Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B2[testIndexes, ]
  trainData <- data_B2[-testIndexes, ]
  
  # Lin reg
  l_reg <- lm(popularity~., data= trainData)
  pred_ch_r <- predict.glm(l_reg, testData[,-14])
  err_lreg_mae[i] <- sum(abs(pred_ch_r-testData$popularity))/length(pred_ch_r)
  err_lreg_mse[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
  
}

# ma error of the mean
sum(err_lreg_mae)/10

# ms error of the mean
sum(err_lreg_mse)/10



#### linear regression with all variables ######

# load the data
data_B_all <- read.csv('Data/dataframe_B_f_and_a.csv', header = TRUE)
data_B_all <- na.omit(data_B_all)

#remove not possible values
data_B_all <- data_B_all[data_B_all$rd_year>500,]


# Randomly shuffle the data
data_B_all <-data_B_all[sample(nrow(data_B_all)),-c(1,2,5,7,17,21,22,23)]

# Scale the timbres
data_B_all[,103:126] <- as.data.frame(scale(data_B_all[,103:126]))

# Create 10 equally size folds
folds <- cut(seq(1,nrow(data_B_all)),breaks=10,labels=FALSE)

# Perform 10 fold cross validation
err_lreg_mae <- err_lreg_mse <- numeric(10)

for(i in 1:10){
  #Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B_all[testIndexes, ]
  trainData <- data_B_all[-testIndexes, ]
  
  # Lin reg
  l_reg <- lm(popularity~., data= trainData)
  pred_ch_r <- predict(l_reg, testData[,-14])
  err_lreg_mae[i] <- sum(abs(pred_ch_r-testData$popularity))/length(pred_ch_r)
  err_lreg_mse[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
}

# ma error of the mean
sum(err_lreg_mae)/10

# ms error of the mean
sum(err_lreg_mse)/10


##### lasso #######

library(glmnet)

#Perform 10 fold cross validation
err_mae <- err_mse <- zeros <-  numeric(10)

for(i in 1:10){
  # Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B_all[testIndexes, ]
  trainData <- data_B_all[-testIndexes, ]
  
  # Lasso
  fit <- cv.glmnet(as.matrix(trainData[,-14]), as.matrix(trainData[ , 14]), alpha = 1) 
  pred_ch_r <- predict(fit, as.matrix(testData[,-14]))
  err_mae[i] <- sum(abs(pred_ch_r-testData$popularity))/length(pred_ch_r)
  err_mse[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
  zeros[i] <- sum(coefficients(fit)==0)/length(coefficients(fit))
}

# ma error of the mean
sum(err_mae)/10

# ms error of the mean
sum(err_mse)/10

# fraction of coeff == 0 mean
sum(zeros)/10


##### random forest cross validation #######

library(randomForest)

#Perform 10 fold cross validation
err_mae <- err_mse <- numeric(10)

for(i in 1:10){
  #Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B_all[testIndexes, ]
  trainData <- data_B_all[-testIndexes, ]
  
  #random forest
  fit <- randomForest(as.matrix(trainData[,-14]), as.matrix(trainData[ , 14]), ntree = 100) 
  pred_ch_r <- predict(fit, as.matrix(testData[,-14]))
  err_mae[i] <- sum(abs(pred_ch_r-testData$popularity))/length(pred_ch_r)
  err_mse[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
}

# ma error of the mean
sum(err_mae)/10

# ms error of the mean
sum(err_mse)/10


##### random forest dependancy plot #######


#random forest
data_B.rf <- randomForest(as.matrix(data_B_all[,-14]), as.matrix(data_B_all[ , 14]), importance = TRUE) 

tiff('Plots/B_dependance_rf.tiff', width = 8, height = 6, units = 'in', res = 200)
varImpPlot(data_B.rf)
dev.off()

tiff('Plots/B_parital_rf_year.tiff', width = 8, height = 6, units = 'in', res = 200)
partialPlot(data_B.rf, data_B_all, x.var = rd_year)
dev.off()

tiff('Plots/B_parital_rf_inst.tiff', width = 8, height = 6, units = 'in', res = 200)
partialPlot(data_B.rf, data_B_all, x.var = instrumentalness)
dev.off()



