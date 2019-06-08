from django.shortcuts import render
from .predictor import predict_minute
from .models import Activity
from custom_users.models import CustomUser

def demo(request):
        activity_labels = [activity.activity_label for activity in Activity.objects.all()][:-1]
        user1 = CustomUser.objects.all()[0]
        user2 = CustomUser.objects.all()[1]
        gps_key=""
        with open ('gps_key.txt') as f:
                gps_key = f.read()
        return render(request, 'demo.html', {'activity_labels':activity_labels, 'user1':user1, 'user2':user2, 'gps_key': gps_key})
