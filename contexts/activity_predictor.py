import csv
import _pickle as cPickle
import numpy as np
import pandas as pd
import sklearn
import glob
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from datetime import datetime

from os import path
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

def load_data():
    filename_queue=glob.glob('./rawdata/data[1-4].csv')
    n_data=[]
    training_set=[]
    test_set=[]
    training_label=[]
    test_label=[]
    label_count=np.zeros(16)

    for filename in filename_queue:
        file=open(filename, newline='')
        
        reader=csv.reader(file)
        header=next(reader)
        
        for row in reader:
            row[4:]=[float(i) for i in row[4:]]
            date=datetime.strptime(row[0],'%Y/%m/%d')
            msec=row[1:3]
            labl=int(row[3])
            label_count[labl]+=1
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
        
                if (label_count[labl]%5!=1):
                    training_set.append(window_feature)
                    training_label.append(labl)
                else:
                    test_set.append(window_feature)
                    test_label.append(labl)

    return training_set, training_label, test_set, test_label

def geT_accuracy(model='RF'):

    trainX, trainY, testX, testY = load_data()
    if path.isfile('models/{}'.format(model)):
        with open('models/{}'.format(model), 'rb') as f:
            clf = cPickle.load(f)
        
    else:
        if model=='SVM': #0.75
            clf = SVC(gamma='scale',tol=0.1)
        elif model=='RF': #0.8275
            clf = RandomForestClassifier(max_depth=20,n_estimators=250)
        elif model=='NB': # 0.7159
            clf = GaussianNB()
        elif model=='KNN': #0.6136
            clf = KNeighborsClassifier(n_neighbors=10)
        clf.fit(trainX,trainY)
        
        with open('models/{}'.format(model), 'wb') as f:
            cPickle.dump(clf, f)
    

    
    pred=clf.predict(testX)

    ohc=OneHotEncoder(categories=[range(16)])
    onehot_pred=pred.reshape(-1,1)
    onehot_pred=ohc.fit_transform(onehot_pred).toarray()

    print(accuracy_score(pred,testY))

geT_accuracy('RF')