import plotly.plotly as py
import plotly.tools as tls
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import (metrics, neighbors, model_selection)

df1 = pd.read_csv("Data/dataframe_A_classification.csv", sep = " ")


X = df1.drop(df1.columns[14], axis=1)
y = df1['chart_random']

# KNN classifier
n_neighbors = 8
knn = neighbors.KNeighborsClassifier(n_neighbors, weights='uniform')
knn.fit(X, y)

# train model with cv 
cv_scores = 1-model_selection.cross_val_score(knn, X, y, cv=6)

# print each cv score (accuracy) and average them
print(cv_scores)
print("cv false classification:" + format(np.mean(cv_scores)))
