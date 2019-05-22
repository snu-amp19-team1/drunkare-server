from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import RawDataRecord
import json

@csrf_exempt
def data(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body.decode("utf-8"))
        print(received_json_data)
        ts = received_json_data['timestamps']
        dt = datetime.fromtimestamp(ts)
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
            timestamp=dt
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
                timestamp=dt
                )
        #TODO: redirect to context for inference
    return HttpResponse(0)

# Create your views here.
