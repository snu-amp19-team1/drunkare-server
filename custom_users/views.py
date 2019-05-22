from django.shortcuts import render
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# Create your views here.
@csrf_exempt
def fetch(request):
        
    users = serializers.serialize('json',CustomUser.objects.all())

    return JsonResponse({"users": users})