#### find the best predictor #####

#load the data
data_B_f <- read.csv('Data/dataframe_b2_features.csv', header = TRUE)
data_B_f<-data_B_f[,-c(1,2,5,7,17,21,22,23)]
set.seed(145)


##### lin regression with only mean #####


#Randomly shuffle the data
data_B2<-data_B_f[sample(nrow(data_B_f)),]

#Create 10 equally size folds
folds <- cut(seq(1,nrow(data_B2)),breaks=10,labels=FALSE)

#Perform 10 fold cross validation
err_lreg <- numeric(10)
for(i in 1:10){
  #Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B2[testIndexes, ]
  trainData <- data_B2[-testIndexes, ]
  
  #Lin reg
  l_reg <- lm(popularity~1, data= trainData)
  pred_ch_r <- predict(l_reg, testData[,-14])
  err_lreg[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
  
}

# error of the mean
sum(err_lreg)/10



##### linear regression with song features #####


#Create 10 equally size folds
folds <- cut(seq(1,nrow(data_B2)),breaks=10,labels=FALSE)

#Perform 10 fold cross validation
err_lreg <- numeric(10)
for(i in 1:10){
  #Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B2[testIndexes, ]
  trainData <- data_B2[-testIndexes, ]
  
  #Lin reg
  l_reg <- lm(popularity~., data= trainData)
  pred_ch_r <- predict(l_reg, testData[,-14])
  err_lreg[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
  
}

# error of linear regression
sum(err_lreg)/10



##### linear regression with all variables ######

#load the data
data_B_all <- read.csv('Data/dataframe_B2_f_and_a.csv', header = TRUE)
data_B_all <- na.omit(data_B_all)
data_B_all <- data_B_all[,-c(1,2,3,6,8,18,22,23,24)]

data_B_all[,103:126] <- as.data.frame(scale(data_B_all[,103:126]))

#Randomly shuffle the data
data_B_all <-data_B_all[sample(nrow(data_B_all)),]

#Create 10 equally size folds
folds <- cut(seq(1,nrow(data_B_all)),breaks=10,labels=FALSE)

#Perform 10 fold cross validation
err_lreg <- numeric(10)

for(i in 1:10){
  # Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B_all[testIndexes, ]
  trainData <- data_B_all[-testIndexes, ]
  
  # Lin reg
  l_reg <- lm(popularity~., data= trainData)
  pred_ch_r <- predict(l_reg, testData[,-14])
  err_lreg[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
  
}

# error of linear regression
sum(err_lreg)/10



##### lasso #####

library(glmnet)

# Perform 10 fold cross validation
err <- numeric(10)

for(i in 1:10){
  # Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B_all[testIndexes, ]
  trainData <- data_B_all[-testIndexes, ]
  
  #Lasso
  fit <- cv.glmnet(as.matrix(trainData[,-14]), as.matrix(trainData[ , 14]), alpha = 1) 
  pred_ch_r <- predict(fit, as.matrix(testData[,-14]))
  err[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
  
}

# error of lasso
sum(err)/10



##### random forest #####


library(randomForest)

#Perform 10 fold cross validation
err <- numeric(10)

for(i in 1:10){
  #Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- data_B_all[testIndexes, ]
  trainData <- data_B_all[-testIndexes, ]
  
  #random forest
  fit <- randomForest(as.matrix(trainData[,-14]), as.matrix(trainData[ , 14]), ntree = 10) 
  pred_ch_r <- predict(fit, as.matrix(testData[,-14]))
  err[i] <- sum((pred_ch_r-testData$popularity)^2)/length(pred_ch_r)
  
}

# error of random forest
sum(err)/10

