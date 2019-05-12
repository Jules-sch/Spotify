### Load the data ####

dataA <- read.csv('Data/dataframe_A_with_song_ana.csv', header = TRUE)
dataA <- na.omit(dataA[,-c(1,5)])

### bagging and boosting ####
set.seed(123)
library(adabag)

# Randomly shuffle the data
dataA2<-dataA[sample(nrow(dataA)),-c(1,5,15,17,19,20)]

# Standardize data except chart_random
dataA2[,-15] <- as.data.frame(scale(dataA2[,-15]))
dataA2$chart_random <- as.factor(dataA2$chart_random)

# Create 10 equally size folds
folds <- cut(seq(1,nrow(dataA2)),breaks=10,labels=FALSE)

# Perform 10 fold cross validation
err_lreg <- numeric(10)
err_boosting <- numeric(10)
for(i in 1:10){
  # Segement your data by fold using the which() function 
  testIndexes <- which(folds==i,arr.ind=TRUE)
  testData <- dataA2[testIndexes, ]
  trainData <- dataA2[-testIndexes, ]

  # Logistic regression
  log_reg <- glm(chart_random~.,
                 family = binomial(link = "logit"), data= trainData)
  pred_ch_r <- predict.glm(log_reg, testData[,-15], type = "response")
  err_lreg[i] <- sum(abs(round(pred_ch_r)-testData$chart_random))/length(pred_ch_r)
  
  # Boosting
  c.boosting <- boosting(chart_random~., data = trainData, mfinal = 11)
  boosting.pred <- predict(c.boosting, newdata = testData)
  err_boosting[i] <- boosting.pred$error
}

# Logistic regression average accuracy
mean(err_lreg)

# Boosting average accuracy
mean(err_boosting)


