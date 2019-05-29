import csv
import os
import _pickle as cPickle
import numpy as np
import pandas as pd
import tensorflow as tf
from os import path
from datetime import datetime
import glob
import random

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout, LSTM, TimeDistributed, ConvLSTM2D
from keras.layers.convolutional import Conv1D, MaxPooling1D

import sklearn
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from .predictor_util import slide_window

module_dir = os.path.dirname(__file__)

# ML models
# input: (60,6,5) feature array 
# slide and reshape to (55,180) 
# infer 
# output: 55 list

# DL models
# ????

def predict_minute(data=None, batch = 55, model_name='RF'):
    
    test_set=[]
    for(x,window) in slide_window(data,1,6): 
        wind=window.reshape(180)
        test_set.append(wind)
    
    # load model
    if path.isfile(module_dir+'/pretrained/{}'.format(model_name)):
        
        with open(module_dir+'/pretrained/{}'.format(model_name), 'rb') as f:
            model = cPickle.load(f)

        if model_name == 'CNN_LSTM':
            data = data.reshape((batch, n_steps, n_length, n_features))
            pred_probs = model.predict(data, batch_size=batch, verbose=0)
            pred = [np.argmax(pred_prob).item() for pred_prob in pred_probs]
            
            return pred
    
        elif model_name =='CONV_LSTM':
            data = data.reshape((batch, n_steps, 1, n_length, n_features))
            pred_probs = model.predict(data, batch_size=batch, verbose=0)
            pred = [np.argmax(pred_prob).item() for pred_prob in pred_probs]
            
            return pred
            
        else:
            
            pred = model.predict(test_set).tolist()
            print(len(pred))
            return pred
        
    else:
        print("model doesn't exist. train the models first.")
        return None


def predict_context():
    filename_queue=glob.glob(module_dir+'/rawdata/compdata[1-3].csv')

    with open(filename_queue[0], newline='') as f:
        reader=csv.reader(f)
        
        for row in reader:
            time=int(row[0]) #minutewise
            context=int(row[1]) #drink 0, eat 1, cafe 2, desk 3
            sensor=int(row[2]) #acc:0 gyro:2
            X_data=row[3:1503]
            Y_data=row[1503:3003]
            Z_data=row[3003:4503]
        print(time,context,sensor)
        
