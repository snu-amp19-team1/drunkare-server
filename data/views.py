from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from contexts.views import update
from .models import RawDataRecord, FeatureRecord, ActivityInferenceRecord
from custom_users.models import CustomUser
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

        # parse POST data
        received_json_data = json.loads(request.body.decode("utf-8"))
        ts = received_json_data['timestamps']
        dt = datetime.fromtimestamp(ts)
        user_id = received_json_data['user_id']
        index = received_json_data['id']
        if 'accel' in received_json_data:
            accel = received_json_data['accel']
            x = accel['x']
            y = accel['y']
            z = accel['z']
            data_type = 0
        elif 'gyro' in received_json_data:
            gyro = received_json_data['gyro']
            x = gyro['x']
            y = gyro['y']
            z = gyro['z']
            data_type = 1
        # save in DB
        try:
            RawDataRecord.objects.create(
                data_type=data_type,
                x=x,
                y=y,
                z=z,
                timestamp=dt,
                user_id= user_id,
                index=index,
            )
        except:
            print("err while saving raw data")
        
        # if both acc & gyro are received, perform inference and update user status
        raw_data = RawDataRecord.objects.filter(user_id=user_id,index=index)

        if raw_data.count()==2:
            
            # fetch data and make window
            accel = raw_data.get(data_type=0)
            gyro = raw_data.get(data_type=1)
            
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

                # save feature
                flattened= feature.flatten().tolist()
                try:
                    feature_record = FeatureRecord.objects.create(
                        feature = flattened,
                        user_id = user_id,
                        raw_data = accel,
                        index=x,
                    )
                except Exception as e:
                    print("err while saving feature", e)
                ndata.append(feature_record.feature)
            
            # if previous raw data exists, add the last 5 seconds data at the front
            prev_raw_data = RawDataRecord.objects.filter(user_id=user_id,index=index-1)
            if prev_raw_data.count() == 2:

                prev_accel = prev_raw_data.get(data_type=0)
                # prev_gyro = prev_raw_data.get(data_type=1)

                # X_acc=ast.literal_eval(prev_accel.x)
                # Y_acc=ast.literal_eval(prev_accel.y)
                # Z_acc=ast.literal_eval(prev_accel.z)
                # X_gyro=ast.literal_eval(prev_gyro.x)
                # Y_gyro=ast.literal_eval(prev_gyro.y)
                # Z_gyro=ast.literal_eval(prev_gyro.z)

                # if previous feature data exists, add the last 5 seconds data at the front
                prev_feature_data = FeatureRecord.objects.filter(user_id=user_id, raw_data=prev_accel)
                if prev_feature_data.count() == 60:
                    try:
                        last_5_features = prev_feature_data.filter(index__gte=55).order_by('index')
                        ndata = [ast.literal_eval(feature.feature) for feature in last_5_features] + ndata

                    except Exception as e:
                        print("err while adding recent 5 sec data", e)

            # perform inference
            ndata=np.array(ndata)
            activities, activities_label = update(ndata)
            # print(activities_label)

            # save activity inference result
            try:
                activity = ActivityInferenceRecord.objects.create(
                    activity_inference=activities,
                    user_id=user_id,
                    index=index,
                )
                recent_activity_record = ActivityInferenceRecord.objects.filter(
                    user_id=user_id,
                    index__gte=index-9,
                )
                activity_count = [0]*16
                for activity_record in recent_activity_record:
                    for activity in ast.literal_eval(activity_record.activity_inference):
                        activity_count[activity]+=1
                custom_user = CustomUser.objects.get(user_id=user_id)
                custom_user.recent_activities = activity_count
                custom_user.last_update = datetime.now()
                custom_user.save()
            except Exception as e:
                print("err while saving activity", e)
            return HttpResponse(1)
            

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

            # save feature
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
        
        # save activity inference result
        try:
            activity = ActivityInferenceRecord.objects.create(
                activity=activities_label,
                user_id=user_id,
            )
        except:
            print("err while saving activity")
        
        
        return HttpResponse(2)
    return HttpResponse(0)