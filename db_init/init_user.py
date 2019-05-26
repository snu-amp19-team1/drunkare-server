from custom_users.models import CustomUser
from contexts.models import Context
from datetime import datetime
CustomUser.objects.all().delete()
users = [
    'shpark',
    'parkj0',
]

recent_activities = [
    '[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]',
    '[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]',
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
        )

CustomUser.objects.create(
    user_name="test",
    user_id = 2,
    recent_activities='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]',
    )