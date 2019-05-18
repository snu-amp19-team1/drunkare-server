import csv
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

def load_data(model):
    filename_queue=glob.glob('./rawdata/data[1-4].csv')
    if model in ['SVM', 'RF', 'NB', 'KNN']:
        n_data=[]
        trainX=[]
        testX=[]
        trainY=[]
        testY=[]
        label_count=np.zeros(16)

        for filename in filename_queue:
            file=open(filename, newline='')
            
            reader=csv.reader(file)
            header=next(reader)
            
            for row in reader:
                row[4:]=[float(i) for i in row[4:]]
                date=datetime.strptime(row[0],'%Y/%m/%d')
                msec=row[1:3]
                label=int(row[3])
                label_count[label]+=1
                for x in range(4):
                    X_acc=list(row[4*i+4+x] for i in range(150))
                    Y_acc=list(row[4*i+604+x] for i in range(150))
                    Z_acc=list(row[4*i+1204+x] for i in range(150))
                    X_gyro=list(row[4*i+1804+x] for i in range(150))
                    Y_gyro=list(row[4*i+2404+x] for i in range(150))
                    Z_gyro=list(row[4*i+3004+x] for i in range(150))
                
                    window=np.array([[X_acc[0:25],X_acc[25:50],X_acc[50:75],X_acc[75:100],X_acc[100:125],X_acc[125:150]],
                        [Y_acc[0:25],Y_acc[25:50],Y_acc[50:75],Y_acc[75:100],Y_acc[100:125],Y_acc[125:150]],
                        [Z_acc[0:25],Z_acc[25:50],Z_acc[50:75],Z_acc[75:100],Z_acc[100:125],Z_acc[125:150]],
                        [X_gyro[0:25],X_gyro[25:50],X_gyro[50:75],X_gyro[75:100],X_gyro[100:125],X_gyro[125:150]],
                        [Y_gyro[0:25],Y_gyro[25:50],Y_gyro[50:75],Y_gyro[75:100],Y_gyro[100:125],Y_gyro[125:150]],
                        [Z_gyro[0:25],Z_gyro[25:50],Z_gyro[50:75],Z_gyro[75:100],Z_gyro[100:125],Z_gyro[125:150]]])
            
                    #5 features  what else?2
                    window_mean=window.mean(axis=-1)
                    window_stddev=window.std(axis=-1)
                    window_median=np.median(window,axis=-1)
                    window_percent25=np.percentile(window,25,axis=-1)
                    window_percent75=np.percentile(window,75,axis=-1)

                    window_feature=np.array([[window_mean],[window_stddev],[window_median],[window_percent25],[window_percent75]])
                    window_feature=window_feature.reshape(180)
            
                    if (label_count[label]%5!=1):
                        trainX.append(window_feature)
                        trainY.append(label)
                    else:
                        testX.append(window_feature)
                        testY.append(label)

        return trainX, trainY, testX, testY
    else:
        dataX = []
        dataY = []
        trainX=[]
        testX=[]
        trainY=[]
        testY=[]
        label_count=np.zeros(16)

        for filename in filename_queue:
            file=open(filename, newline='')
            reader=csv.reader(file)
            header=next(reader)
            read = list(reader)
            random.shuffle(read)

            for row in read:
                row[4:]=[float(i) for i in row[4:]]
                date=datetime.strptime(row[0],'%Y/%m/%d')
                label=int(row[3])
                label_count[label]+=1

                for x in range(4):
                    X_acc=list(row[4*i+4+x] for i in range(150))
                    Y_acc=list(row[4*i+604+x] for i in range(150))
                    Z_acc=list(row[4*i+1204+x] for i in range(150))
                    X_gyro=list(row[4*i+1804+x] for i in range(150))
                    Y_gyro=list(row[4*i+2404+x] for i in range(150))
                    Z_gyro=list(row[4*i+3004+x] for i in range(150))

                    window=np.array([X_acc[0:150],Y_acc[0:150],Z_acc[0:150], X_gyro[0:150], Y_gyro[0:150], Z_gyro[0:150]])
                    window = np.transpose(window)

                    if (label_count[label]%5!=1):
                        trainX.append(window)
                        trainY.append(label)
                    else:
                        testX.append(window)
                        testY.append(label)

        trainX = np.stack(trainX, axis = 0)
        trainY = np.stack(trainY, axis = 0)
        testX = np.stack(testX, axis = 0)
        testY = np.stack(testY, axis = 0)
        #one-hot encode
        trainY = to_categorical(trainY)
        testY = to_categorical(testY)

        return trainX, trainY, testX, testY


def create_model(model, trainX=None, trainY=None):
    
    if model=='SVM': #0.75
        clf = SVC(gamma='scale',tol=0.1)
    elif model=='RF': #0.8275
        clf = RandomForestClassifier(max_depth=20,n_estimators=250)
    elif model=='NB': # 0.7159
        clf = GaussianNB()
    elif model=='KNN': #0.6136
        clf = KNeighborsClassifier(n_neighbors=10)
    else:
        n_timesteps, n_features, n_outputs = trainX.shape[1], trainX.shape[2], trainY.shape[1]
        
        if model=='CNN_LSTM':
            n_lstm_cell = 128 #number of lstm cells
            epochs=32 #training epoch
            n_fc_cell = 32 #numer of fc layer cells
            dropout = 0.4 #dropout rate
            pool_size=1
            batch_size = 32
            n_steps, n_length = 10,15
            
            clf = Sequential()
            clf.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu'), input_shape=(None,n_length,n_features)))
            clf.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu')))
            clf.add(TimeDistributed(Dropout(dropout)))
            clf.add(TimeDistributed(MaxPooling1D(pool_size=pool_size)))
            clf.add(TimeDistributed(Flatten()))
            clf.add(LSTM(n_lstm_cell))
            clf.add(Dropout(dropout))
            clf.add(Dense(n_fc_cell, activation='relu'))
            clf.add(Dense(n_outputs, activation='softmax'))
            clf.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        elif model=='CONV_LSTM':
            dropout = 0.4
            n_fc_cell = 32
            epochs= 20
            batch_size=32
            n_steps, n_length = 10,15

            clf = Sequential()
            clf.add(ConvLSTM2D(filters=64, kernel_size=(1,3), activation='relu', input_shape=(n_steps, 1, n_length, n_features)))
            clf.add(Dropout(dropout))
            clf.add(Flatten())
            clf.add(Dense(n_fc_cell, activation='relu'))
            clf.add(Dense(n_outputs, activation='softmax'))
            clf.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        
    return clf
        

def get_accuracy(model='RF'):
    
    trainX, trainY, testX, testY = load_data(model)
    
    if path.isfile('pretrained/{}'.format(model)):
        with open('pretrained/{}'.format(model), 'rb') as f:
            clf = cPickle.load(f)
    
        
    else:
        if model =='CNN_LSTM':
            clf = create_model(model, trainX, trainY)
            clf.fit(trainX, trainY, epochs=32, batch_size=32, verbose=0)
        elif model== 'CONV_LSTM':
            clf = create_model(model, trainX, trainY)
            clf.fit(trainX, trainY, epochs=32, batch_size=32, verbose=0)
        else:
            clf = create_model(model)
            clf.fit(trainX,trainY)

        with open('pretrained/{}'.format(model), 'wb') as f:
            cPickle.dump(clf, f)
    

    if model in ['CNN_LSTM', 'CONV_LSTM']:
        _, accuracy = model.evaluate(testX, testY, batch_size=32, verbose=0)
        print(accuracy)
    else:
        pred=clf.predict(testX)
        ohc=OneHotEncoder(categories=[range(16)])
        onehot_pred=pred.reshape(-1,1)
        onehot_pred=ohc.fit_transform(onehot_pred).toarray()
        print(accuracy_score(pred,testY))

get_accuracy('CNN_LSTM')