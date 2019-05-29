import os
import _pickle as cPickle
import numpy as np
from os import path
import glob

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
    print(len(test_set))
    
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
    glob.glob(module_dir+'/rawdata/compdata[1-3].csv')
    #drink 0, eat 1, cafe 2, desk 3
    C

        
