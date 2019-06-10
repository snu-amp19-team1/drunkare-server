import os
import _pickle as cPickle
import numpy as np
from os import path
import glob

from sklearn import preprocessing
from .predictor_util import slide_window, stdmean

module_dir = os.path.dirname(__file__)

# ML models
# input: (60,6,5) feature array 
# slide and reshape to (55,180)
# infer 
# output: 55 list

# DL models
# ????

def predict_minute(data=None, batch = 55, model_name='ETC'):
    
    test_set=[]
    for _,window in slide_window(data,3,6): 
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
            pred=[]
            stdMean = []
            
            # for postprocessing
            for i in test_set:
                stdMean.append(stdmean(i))
            stdMean = np.array(stdMean)
            np.set_printoptions(precision=2)

            pred_probs = model.predict_proba(test_set)
            for j in pred_probs:
                if np.max(j)<0.2: #확률 0.3미만이면 idle
                    pred.append(10)
                else:
                    if np.argmax(j)==8:
                        #print('label : ',np.argmax(j), 'probability : ',np.max(j))
                        if(np.max(j)<0.3):
                            pred.append(10)
                        else:
                            pred.append(8)
                    else:
                        if np.argmax(j)==0:
                        #print('label : ',np.argmax(j), 'probability : ',np.max(j))
                            if(np.max(j)<0.35):
                                pred.append(10)
                            else:
                                pred.append(0)
                        else:
                            pred.append(np.argmax(j))     
            
            # postprocessing
            pred2 = []
            for i,p in enumerate(pred):
                if float(stdMean[i])>=0.5:
                    pred2.append(pred[i])
                else:
                    pred2.append(10)
            return pred2
        
    else:
        print("model doesn't exist. train the models first.")
        return None


def predict_context(data=None, model_name='rf'):
    # print('predicting context') #drink 0, eat 1, cafe 2, desk 3
    if len(data) == 199:
        data.append(10)
    data = np.array(data).reshape(10,20)
    
    context_input = []
    for minute in data:
        
        activity_count=np.zeros(11)
        for activity in minute:
            try:
                activity_count[activity]+=1
            except:
                print("activity label out of range")
        context_input.append(activity_count)
    
    context_input = np.array(context_input)
    # print(context_input.shape)

    context = 0
    if path.isfile(module_dir+'/pretrained/complex_{}.sav'.format(model_name)):
        with open(module_dir+'/pretrained/complex_{}.sav'.format(model_name), 'rb') as f:
            model = cPickle.load(f)
            context_input = context_input.reshape(1,-1)
            context = model.predict(context_input)[0]

    return context

        
