import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .activity_predictor import predict_minute
from .models import Context, Activity
from custom_users.models import CustomUser

def update(data):
        activities = predict_minute(data,model_name="RF")
        activities_label = [Activity.objects.get(activity_id=pred).activity_label for pred in activities]

        return activities, activities_label

def demo(request):
        activity_labels = [activity.activity_label for activity in Activity.objects.all()]
        user1 = CustomUser.objects.all()[0]
        user2 = CustomUser.objects.all()[1]

        return render(request, 'demo.html', {'activity_labels':activity_labels, 'user1':user1, 'user2':user2})
