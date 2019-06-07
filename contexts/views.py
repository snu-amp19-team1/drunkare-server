from django.shortcuts import render
from .predictor import predict_minute
from .models import Activity
from custom_users.models import CustomUser

def demo(request):
        activity_labels = [activity.activity_label for activity in Activity.objects.all()]
        user1 = CustomUser.objects.all()[0]
        user2 = CustomUser.objects.all()[1]

        return render(request, 'demo.html', {'activity_labels':activity_labels, 'user1':user1, 'user2':user2, 'gps_key': 'AIzaSyDwLZCrnSp5iiWtoRVYxI0J1we0QtAyT0c '})
