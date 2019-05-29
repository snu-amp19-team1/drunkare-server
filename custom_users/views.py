from .models import CustomUser
from contexts.models import Context
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

# Create your views here.
@csrf_exempt
def fetch(request):
    users = serializers.serialize('json',CustomUser.objects.filter(user_id__lte=1))
    users = json.loads(users)
    for user in users:
        label=Context.objects.get(context_id=user['fields']['current_context'])
        user['fields']['current_context']=str(label)
    return JsonResponse({"users": json.dumps(users)})