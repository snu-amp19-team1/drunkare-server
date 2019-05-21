import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .activity_predictor import predict_activity, predict_context
from .models import Context, Activity

@csrf_exempt
def infer(request):
    if request.method == "POST":
        print("infering")
        
        activities = predict_activity(model_name="RF")
        activities_dump = json.dumps(activities)

        try:
                activities_label = [Activity.objects.get(activity_id=pred).activity_label for pred in activities]
                print(activities_label)
        except:
                pass
        
        # context = predict_context()

        return JsonResponse({"activities":activities_dump})

def demo(request):
        try:
                user_id = int(request.GET.get('user_id'))
        except:
                pass
        return render(request, 'demo.html')
