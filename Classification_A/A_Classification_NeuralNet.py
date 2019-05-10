import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow.keras as keras
from sklearn import model_selection

df1 = pd.read_csv("Data/dataframe_A_classification.csv", sep = " ")

X = np.array(df1.drop(['chart_random'], axis=1))
y = np.array(df1['chart_random'])
y = keras.utils.to_categorical(y)

# function builds the model
def build_model():
    network = keras.models.Sequential()
    network.add(keras.layers.Dense(40, activation='relu', input_shape=(14,)))
    network.add(keras.layers.Dense(20, activation='relu'))
    network.add(keras.layers.Dense(2, activation='softmax'))
    network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
    return network


# create the k-fold splits
k = 10
kf = model_selection.KFold(n_splits=k)
kf.get_n_splits(X)  # create the splits

num_epochs = 3
err = []

i = 1
for train_idx, val_idx in kf.split(X):
    print('processing fold #', i)
    partial_train_data, val_data = X[train_idx], X[val_idx]
    partial_train_targets, val_targets = y[train_idx], y[val_idx]
    
    model = build_model()
    model.fit(partial_train_data, partial_train_targets,
              epochs=num_epochs, batch_size=1, verbose=0)
    
    y_pred = model.predict(val_data, verbose=0)
    y_pred_n =  np.argmax(y_pred, axis = 1)
    y_true_n = np.argmax(val_targets, axis = 1)
    err.append(sum(abs(y_pred_n-y_true_n))/len(y_true_n))
    i += 1
    
print('Error ', np.mean(err))

