from contexts.models import Activity
Activity.objects.all().delete()
activities = [
    'touching face', 
    'jotting',
    'clinking',
    'drinking (glass w/o handle)',
    'pulling out tissue',
    'drinking (glass w/ handle)',
    'eating with a spoon',
    'eating with chopsticks',
    'eating with a fork',
    'stirring',
    ]

for i,activity in enumerate(activities):
    Activity.objects.create(activity_label=activity,activity_id = i)