#drink 0, eat 1, cafe 2, desk 3
from contexts.models import Context
from custom_users.models import CustomUser
CustomUser.objects.all().delete()
Context.objects.all().delete()
contexts = [
    'drinking',
    'eating',
    'cafe',
    'desk',
    ]

for i,context in enumerate(contexts):
    Context.objects.create(context_label=context,context_id = i)