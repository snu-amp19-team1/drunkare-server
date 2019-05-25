from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from contexts.views import update
from .models import RawDataRecord, FeatureRecord, ActivityRecord
import requests
import json
import ast
import numpy as np


def feature_extraction(window):
    mean=window.mean(axis=-1)
    stddev=window.std(axis=-1)
    median=np.median(window,axis=-1)
    percent25=np.percentile(window,25,axis=-1)
    percent75=np.percentile(window,75,axis=-1)
    return(np.array([mean,stddev,median,percent25,percent75]))

@csrf_exempt
def data(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body.decode("utf-8"))
        
        # save in DB
        ts = received_json_data['timestamps']
        dt = datetime.fromtimestamp(ts)
        user_id = received_json_data['user_id']
        index = received_json_data['id']
        if 'accel' in received_json_data:
            accel = received_json_data['accel']
            x = accel['x']
            y = accel['y']
            z = accel['z']            
            RawDataRecord.objects.create(
                data_type=0,
                x=x,
                y=y,
                z=z,
                timestamp=dt,
                user_id= user_id,
                index=index,
            )
            
        elif 'gyro' in received_json_data:
            gyro = received_json_data['gyro']
            x = gyro['x']
            y = gyro['y']
            z = gyro['z']
            RawDataRecord.objects.create(
                data_type=1,
                x=x,
                y=y,
                z=z,
                timestamp=dt,
                user_id = user_id,
                index=index,
            )

        raw_data = RawDataRecord.objects.filter(user_id=user_id,index=index)
        if raw_data.count()==2:
            
            accel = raw_data.get(data_type=0)
            gyro = raw_data.get(data_type=1)
            
            # parse and make window
            X_acc=ast.literal_eval(accel.x)
            Y_acc=ast.literal_eval(accel.y)
            Z_acc=ast.literal_eval(accel.z)
            X_gyro=ast.literal_eval(gyro.x)
            Y_gyro=ast.literal_eval(gyro.y)
            Z_gyro=ast.literal_eval(gyro.z)
            
            ndata=[]
            for x in range(0,60): 
                wind=np.array([X_acc[25*x:25*x+25],Y_acc[25*x:25*x+25],Z_acc[25*x:25*x+25],
                            X_gyro[25*x:25*x+25],Y_gyro[25*x:25*x+25],Z_gyro[25*x:25*x+25]])  
                feature=feature_extraction(wind)
                feature=feature.reshape(6,5)
                ndata.append(feature)

                # save feature
                flattened= feature.flatten()
                try:
                    feature_record = FeatureRecord.objects.create(
                        feature = flattened,
                        user_id = user_id,
                    )
                except:
                    print("err")
                ndata.append(feature_record.feature)

            ndata=np.array(ndata)
            # TODO: infer with accumulated data and update user table
            activities = update(ndata)
            print(activities)

            return JsonResponse({"activities":activities})

    if request.method == "GET":
        
        with open ('json_sample.json') as f:
            f_data = f.read()

        received_json_data = json.loads(f_data)

        
        ts = received_json_data['timestamps']
        dt = datetime.fromtimestamp(ts)
        user_id = received_json_data['user_id']
        index = received_json_data['id']
          
        accel = received_json_data['gyro']
        x = accel['x']
        y = accel['y']
        z = accel['z']
        
        accel = RawDataRecord(
            data_type=0,
            x=x,
            y=y,
            z=z,
            timestamp=dt,
            user_id= user_id,
            index=index,
        )
        
        gyro = received_json_data['gyro']
        x = gyro['x']
        y = gyro['y']
        z = gyro['z']
        gyro = RawDataRecord(
            data_type=1,
            x=x,
            y=y,
            z=z,
            timestamp=dt,
            user_id = user_id,
            index=index,
        )
        
        # parse and make window
        X_acc=accel.x
        Y_acc=accel.y
        Z_acc=accel.z
        X_gyro=gyro.x
        Y_gyro=gyro.y
        Z_gyro=gyro.z
        
        ndata=[]
        for x in range(0,60): 
            wind=np.array([X_acc[25*x:25*x+25],Y_acc[25*x:25*x+25],Z_acc[25*x:25*x+25],
                        X_gyro[25*x:25*x+25],Y_gyro[25*x:25*x+25],Z_gyro[25*x:25*x+25]])  
            
            feature=feature_extraction(wind)
            feature=feature.reshape(6,5)
            flattened= feature.flatten()
            try:
                feature_record = FeatureRecord.objects.create(
                    feature = flattened,
                    user_id = user_id,
                )
            except:
                print("err")
            ndata.append(feature_record.feature)
        
        ndata=np.array(ndata)
        activities, activities_label = update(ndata)
        print(activities_label)
        ActivityRecord.objects.create(
            activity=activities,
            user_id=user_id,
        )
        
        return JsonResponse({"activities":activities_label})
    return HttpResponse(0)