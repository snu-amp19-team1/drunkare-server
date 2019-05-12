from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def data(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body.decode("utf-8"))
        print(received_json_data)
    return HttpResponse(0)

# Create your views here.
