import json
from django.shortcuts import render
from django.http import JsonResponse
from .activity_predictor import predict_activity

# Create your views here.
def infer(request):
    print("infering")
    result = predict_activity(model_name="CONV_LSTM")
    result_dump = json.dumps(result)
    return JsonResponse({"result":result_dump})