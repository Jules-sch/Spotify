
# load data
dataA <- read.csv('Data/dataframe_A.csv', header = TRUE)
dataA <- dataA[,-4]
dataA$chart_random_f[dataA$chart_random==0] <- "random"
dataA$chart_random_f[dataA$chart_random==1] <- "chart"
dataA$chart_random_f <- as.factor(dataA$chart_random_f)


##### find differences between two groups #######

# logistic regression
l_reg1 <- glm(chart_random~acousticness+
                instrumentalness+loudness+
                speechiness+valence,family = binomial(link = "logit"), data= dataA)
exp(l_reg1$coefficients)
summary(l_reg1)

# test if larger model is better
l_reg2 <- glm(chart_random~acousticness+instrumentalness+loudness+tempo+
                speechiness+valence,family = binomial(link = "logit"), data= dataA)
anova(l_reg1,l_reg2, test = "Chisq")

# decision tree
require( partykit)
rt <- ctree(chart_random_f~acousticness+danceability+duration+
              valence+mode+instrumentalness+loudness+speechiness, data=dataA, maxdepth = 4)
plot(rt, cex = 0.5)


###### predict best classifier #######

# Randomly shuffle the data
dataA2<-dataA[sample(nrow(dataA)),-c(1,5,15,17,19,20,22)]

# Standardize data except chart_random
dataA2[,-15] <- as.data.frame(scale(dataA2[,-15]))
#Create 10 equally size folds
folds <- cut(seq(1,nrow(dataA2)),breaks=10,labels=FALSE)

# Perform 10 fold cross validation
err_lreg <- numeric(10)
for(i in 1:10){
  #Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- dataA2[testIndexes, ]
  trainData <- dataA2[-testIndexes, ]
  
  # Logistic regression
  log_reg <- glm(chart_random~.,
                 family = binomial(link = "logit"), data= trainData)
  pred_ch_r <- predict.glm(log_reg, testData[,-15], type = "response")
  err_lreg[i] <- sum(abs(round(pred_ch_r)-testData$chart_random))/length(pred_ch_r)
  
}

# logistic regression error
sum(err_lreg)/10


### bagging boosting ###
library(adabag)

# Randomly shuffle the data
dataA2<-dataA[sample(nrow(dataA)),-c(1,5,15,17,19,20,22)]

# Standardize data except chart_random
dataA2[,-15] <- as.data.frame(scale(dataA2[,-15]))
dataA2$chart_random <- as.factor(dataA2$chart_random)

# Create 10 equally size folds
folds <- cut(seq(1,nrow(dataA2)),breaks=10,labels=FALSE)

# Perform 10 fold cross validation
err_bagging <- numeric(10)
err_boosting <- numeric(10)
for(i in 1:10){
  # Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- dataA2[testIndexes, ]
  trainData <- dataA2[-testIndexes, ]
  
  # Bagging
  c.bagging <- bagging(chart_random~., data = trainData, mfinal = 11)
  bagging.pred <- predict(c.bagging, newdata = testData)
  err_bagging[i] <- bagging.pred$error
  
  # Boosting
  c.boosting <- boosting(chart_random~., data = trainData, mfinal = 11)
  boosting.pred <- predict(c.boosting, newdata = testData)
  err_boosting[i] <- boosting.pred$error
}

# Bagging average accuracy
mean(err_bagging)

# Boosting average accuracy
mean(err_boosting)

