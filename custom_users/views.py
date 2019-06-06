from .models import CustomUser
from contexts.models import Context, Activity
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from custom_users.models import CustomUser
from django.utils.timezone import make_aware
import json, ast
from datetime import timedelta

# Create your views here.
@csrf_exempt
def web(request):
    users = serializers.serialize('json',CustomUser.objects.filter(user_id__lte=1))
    users = json.loads(users)
    for user in users:
        try:
            label=Context.objects.get(context_id=user['fields']['current_context'])
            user['fields']['current_context']=str(label)
        except:
            user['fields']['current_context']=''
    return JsonResponse({"users": json.dumps(users)})


# Create your views here.
@csrf_exempt
def app(request):
    user_id = request.GET['user_id']
    custom_user = CustomUser.objects.get(user_id=user_id)
    try:
        context = custom_user.current_context.context_label
    except:
        context = ''
    activity_labels = [activity.activity_label for activity in Activity.objects.all()]
    activity_probs = ast.literal_eval(custom_user.recent_activities)
    
    activity_dict = dict(zip(activity_labels, activity_probs))
    top3 = sorted(activity_dict.items() ,  key=lambda x: -x[1])[:3]
    time = (custom_user.last_update+timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
    loc = custom_user.current_location
    return JsonResponse({'context':context, 'top3':top3, 'time':time, 'loc':loc})