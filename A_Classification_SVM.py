import plotly.plotly as py
import plotly.tools as tls
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import (metrics, neighbors, model_selection,svm)

# read data
df1 = pd.read_csv("Data/dataframe_A_classification.csv", sep = " ")

# drop the id
df1 = (df1.drop(df1.columns[0], axis=1))

X = np.array(df1.drop(['chart_random'], axis = 1))
y = np.array(df1['chart_random'])

# 10 folds cross validation
kf = model_selection.KFold(n_splits = 10)
kf.get_n_splits(X)

err = np.zeros(10)

i = 0
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    clf = svm.SVC(gamma='scale')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    err[i] = sum(abs(y_test-y_pred))/len(y_test)
    i +=1
    
print(sum(err)/10)



#### do the same with song ana data ####

# read dataframe with song analysis
df1 = pd.read_csv("Data/dataframe_A_with_sa_scaled.csv", sep = ",")

# drop the id
df1 = (df1.drop(df1.columns[0], axis=1))

# drop the timbre variances, pitch variances and pitch correlations
cols = list(range(15,26))+list(range(31,97))+list(range(115,127))
df1 = (df1.drop(df1.columns[cols], axis=1))

X = np.array(df1.drop(['chart_random'], axis=1))
y = np.array(df1['chart_random'])

# 10 folds cross validation
kf = model_selection.KFold(n_splits = 10)
kf.get_n_splits(X)

err = np.zeros(10)

i = 0
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    clf = svm.SVC(gamma = 'scale')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    err[i] = sum(abs(y_test-y_pred))/len(y_test)
    i +=1
    
print(sum(err)/10)
