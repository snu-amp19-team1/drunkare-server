from custom_users.models import CustomUser
from contexts.models import Context
from datetime import datetime

users = [
    'shpark',
    'parkj0',
]

recent_activities = [
    '[0,4,5,1,2,0,6,0,0,4,5,1,2,0,6,0]',
    '[5,0,1,2,1,2,4,0,6,0,0,6,0,0,4,5]',
]

contexts=[
    Context.objects.get(context_id=3),
    Context.objects.get(context_id=2),
]

for i,user in enumerate(users):
    CustomUser.objects.create(
        user_name=user,
        user_id = i,
        recent_activities=recent_activities[i],
        current_context=contexts[i],
        last_update=datetime.now(),
        )