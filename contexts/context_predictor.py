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

module_dir = os.path.dirname(__file__)

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
        

predict_context()