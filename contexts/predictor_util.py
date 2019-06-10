import csv
import os
import _pickle as cPickle
import numpy as np
from os import path
from datetime import datetime
import glob
import random

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout, LSTM, TimeDistributed, ConvLSTM2D
from keras.layers.convolutional import Conv1D, MaxPooling1D

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

module_dir = os.path.dirname(__file__)

def stdmean(window):
    RMS_window=[]
    for i in range(0,180,6):
        RMS_window.append(float(window[i]))
    RMS_window=np.array(RMS_window)
    return RMS_window.std(axis=-1)

def load_data(model_name, n_steps=None, n_length=None, n_features=None):
    filename_queue=glob.glob(module_dir+'/rawdata/data[1-5].csv')
    if model_name in ['SVM', 'RF', 'NB', 'KNN']:
        trainX=[]
        testX=[]
        trainY=[]
        testY=[]
        label_count=np.zeros(16)

        for filename in filename_queue:
            file=open(filename, newline='')
            
            reader=csv.reader(file)
            next(reader)
            read = list(reader)
            random.shuffle(read)
            
            for row in read:
                row[4:]=[float(i) for i in row[4:]]
                datetime.strptime(row[0],'%Y/%m/%d')
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
        trainX=[]
        testX=[]
        trainY=[]
        testY=[]
        label_count=np.zeros(16)
        for filename in filename_queue:
            file=open(filename, newline='')
            reader=csv.reader(file)
            next(reader)
            read = list(reader)
            random.shuffle(read)

            for row in read:
                row[4:]=[float(i) for i in row[4:]]
                datetime.strptime(row[0],'%Y/%m/%d')
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


def create_model(model_name, n_features=None, n_outputs=None):
    
    if model_name in ['SVM', 'RF', 'NB', 'KNN']:
        if model_name=='SVM': #0.75
            model = SVC(gamma='scale',tol=0.1)
        elif model_name=='RF': #0.8275
            model = RandomForestClassifier(max_depth=20,n_estimators=250)
        elif model_name=='NB': # 0.7159
            model = GaussianNB()
        elif model_name=='KNN': #0.6136
            model = KNeighborsClassifier(n_neighbors=10)
        return model
    else:
        
        
        if model_name=='CNN_LSTM':
            n_steps, n_length = 10,15
            n_lstm_cell = 128 #number of lstm cells
            n_fc_cell = 32 #numer of fc layer cells
            dropout = 0.4 #dropout rate
            pool_size=1
            
            model = Sequential()
            model.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu'), input_shape=(None,n_length,n_features)))
            model.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu')))
            model.add(TimeDistributed(Dropout(dropout)))
            model.add(TimeDistributed(MaxPooling1D(pool_size=pool_size)))
            model.add(TimeDistributed(Flatten()))
            model.add(LSTM(n_lstm_cell))
            model.add(Dropout(dropout))
            model.add(Dense(n_fc_cell, activation='relu'))
            model.add(Dense(n_outputs, activation='softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        elif model_name=='CONV_LSTM':
            n_steps, n_length = 10,15
            dropout = 0.4
            n_fc_cell = 32
            n_steps, n_length = 10,15

            model = Sequential()
            model.add(ConvLSTM2D(filters=64, kernel_size=(1,3), activation='relu', input_shape=(n_steps, 1, n_length, n_features)))
            model.add(Dropout(dropout))
            model.add(Flatten())
            model.add(Dense(n_fc_cell, activation='relu'))
            model.add(Dense(n_outputs, activation='softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        return model, n_steps, n_length
        

def get_accuracy(model_name='RF'):
    
    trainX, trainY, testX, testY = load_data(model_name)
    
    # first try load
    
    if path.isfile(module_dir+'/pretrained/{}'.format(model_name)):
        if model_name in ['CNN_LSTM', 'CONV_LSTM']:
            n_features, n_outputs = trainX.shape[2], trainY.shape[1]
            _, n_steps, n_length = create_model(model_name, n_features, n_outputs)


        with open(module_dir+'/pretrained/{}'.format(model_name), 'rb') as f:
            model = cPickle.load(f)
        
        
    else:

        # train model
        if model_name == 'CNN_LSTM':
            n_features, n_outputs = trainX.shape[2], trainY.shape[1]
            model, n_steps, n_length = create_model(model_name, n_features, n_outputs)

            trainX = trainX.reshape((trainX.shape[0], n_steps, n_length, n_features))
            model.fit(trainX, trainY, epochs=32, batch_size=32, verbose=0)

        elif model_name == 'CONV_LSTM':
            n_features, n_outputs = trainX.shape[2], trainY.shape[1]
            model, n_steps, n_length = create_model(model_name, n_features, n_outputs)
            
            trainX = trainX.reshape((trainX.shape[0], n_steps, 1, n_length, n_features))
            model.fit(trainX, trainY, epochs=32, batch_size=32, verbose=0)
        else:
            model = create_model(model_name)
            model.fit(trainX,trainY)

        # save model
        with open(module_dir+'/pretrained/{}'.format(model_name), 'wb') as f:
            cPickle.dump(model, f)
    

    if model_name == 'CNN_LSTM':
        testX = testX.reshape((testX.shape[0], n_steps, n_length, n_features))
        _, accuracy = model.evaluate(testX, testY, batch_size=32, verbose=0)
        print(accuracy)

    elif model_name =='CONV_LSTM':
        testX = testX.reshape((testX.shape[0], n_steps, 1, n_length, n_features))
        _, accuracy = model.evaluate(testX, testY, batch_size=32, verbose=0)
        print(accuracy)

        
    else:
        pred=model.predict(testX)
        ohc=OneHotEncoder(categories=[range(16)])
        onehot_pred=pred.reshape(-1,1)
        onehot_pred=ohc.fit_transform(onehot_pred).toarray()
        print(accuracy_score(pred,testY))

def slide_window(data,stepSize,windowSize):
    for x in range(0,len(data)-windowSize+1,stepSize):
        yield(x,data[x:x+windowSize])