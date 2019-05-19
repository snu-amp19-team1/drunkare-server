import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .activity_predictor import predict_activity

@csrf_exempt
def infer(request):
    if request.method == "POST":
        print("infering")
        result = predict_activity(model_name="RF")
        result_dump = json.dumps(result)
        return JsonResponse({"result":result_dump})
    