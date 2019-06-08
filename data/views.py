from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import time
from django.utils.timezone import make_aware
from contexts.predictor import predict_minute,predict_context
from .models import RawDataRecord, FeatureRecord, ActivityInferenceRecord
from contexts.models import Context
from custom_users.models import CustomUser
from math import sqrt, cos
import requests
import json
import ast
import time
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
        dt = make_aware(datetime.fromtimestamp(ts))
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
        
        # if index = 0, check if this is the beginning of a new sequence
        if index == 0:
            if RawDataRecord.objects.filter(user_id=user_id,index=index).count() >= 2:
                RawDataRecord.objects.filter(user_id=user_id).delete()
                FeatureRecord.objects.filter(user_id=user_id).delete()
                ActivityInferenceRecord.objects.filter(user_id=user_id).delete()
                print("DB initialized")
        
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
            
            # if previous raw data exists, add the last 3 seconds data at the front
            prev_raw_data = RawDataRecord.objects.filter(user_id=user_id,index=index-1)
            if prev_raw_data.count() == 2:

                prev_accel = prev_raw_data.get(data_type=0)
               
                # if previous feature data exists, add the last 3 seconds data at the front
                prev_feature_data = FeatureRecord.objects.filter(user_id=user_id, raw_data=prev_accel)
                if prev_feature_data.count() == 60:
                    try:
                        last_3_features = prev_feature_data.filter(index__gte=57).order_by('index')
                        ndata = [ast.literal_eval(feature.feature) for feature in last_3_features] + ndata

                    except Exception as e:
                        print("err while adding recent 3 sec data", e)

            # perform activity inference
            ndata=np.array(ndata)
            activities = predict_minute(ndata)
            
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
                activity_count = [0]*11
                for activity_record in recent_activity_record:
                    for activity in ast.literal_eval(activity_record.activity_inference):
                        activity_count[activity]+=1
                custom_user = CustomUser.objects.get(user_id=user_id)
                custom_user.recent_activities = activity_count
                custom_user.last_update = make_aware(datetime.now())
                custom_user.save()
            except Exception as e:
                print("err while saving activity", e)

            # perform context detection
            activities_history = []
            for record in ActivityInferenceRecord.objects.filter(user_id=user_id).order_by('-record_id')[:10]:
                activities_history = ast.literal_eval(record.activity_inference) + activities_history
            
            if len(activities_history) in [199,200]:
                try:
                    context = predict_context(activities_history)
                    custom_user = CustomUser.objects.get(user_id=user_id)
                    custom_user.current_context = Context.objects.get(context_id = context)
                    custom_user.save()
                    print("predicted")
                    
                except:
                    print("error while updating context")

        return HttpResponse(raw_data.count())
            

    if request.method == "GET":
        user_id = 1
        activities_history = []
        for record in ActivityInferenceRecord.objects.filter(user_id=user_id).order_by('-record_id')[:10]:
            activities_history = ast.literal_eval(record.activity_inference) + activities_history
    
        if len(activities_history)==200:
            context = predict_context(activities_history)
            return HttpResponse(context)
        for i in range (20):
            print(i)
            for u_i in range(1):
                np.random.seed(i)
                test_json = {}
                test_json['timestamps'] = time.time()
                test_json['id'] = i
                test_json['user_id'] = u_i
                test_json['gyro']={}
                test_json['gyro']['x'] =  np.random.randn(1500).tolist()
                test_json['gyro']['y'] =  np.random.randn(1500).tolist()
                test_json['gyro']['z'] =  np.random.randn(1500).tolist()
                requests.post('http://lynx.snu.ac.kr:8081/data/',json.dumps(test_json))
                
                test_json = {}
                test_json['timestamps'] = time.time()
                test_json['id'] = i
                test_json['user_id'] = u_i
                test_json['accel']={}
                test_json['accel']['x'] = np.random.randn(1500).tolist()
                test_json['accel']['y'] = np.random.randn(1500).tolist()
                test_json['accel']['z'] = np.random.randn(1500).tolist()
                requests.post('http://lynx.snu.ac.kr:8081/data/',json.dumps(test_json))
            

            time.sleep(3)
            
            
        
        return HttpResponse(0)

@csrf_exempt
def gps(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body.decode("utf-8"))
        ts = received_json_data['timestamp']
        dt = make_aware(datetime.fromtimestamp(ts))
        user_id = received_json_data['user_id']
        latitude = received_json_data['latitude']
        longitude = received_json_data['longitude']
        
        custom_user = CustomUser.objects.get(user_id=user_id)
        try:
            last_lat, last_long = custom_user.current_location.split(',')
            last_lat = float(last_lat)
            last_long = float(last_long)
            R = 6371  # radius of the earth in km
            x = (longitude - last_long) * cos( 0.5*(latitude + last_lat) )
            y = latitude - last_lat
            d = R * sqrt( x*x + y*y )
            if d >= 3:
                custom_user.is_still = 0
            else:
                custom_user.is_still = 1
            
        except Exception as e:
            print(e)
        custom_user.current_location = str(latitude)+','+str(longitude)
        custom_user.last_update = dt
        custom_user.save()

    if request.method == "GET":
        test_json = {
            "user_id": 1,
            "timestamp": time.time(),
            "latitude": 37.450057, 
            "longitude": 126.952549
            }
        requests.post('http://lynx.snu.ac.kr:8081/data/gps',json.dumps(test_json))
        test_json = {
            "user_id": 0,
            "timestamp": time.time(),
            "latitude": 37.448600,  
            "longitude": 126.952570
            }
        requests.post('http://lynx.snu.ac.kr:8081/data/gps',json.dumps(test_json))
    return HttpResponse(0)