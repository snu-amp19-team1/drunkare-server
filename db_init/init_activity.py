from contexts.models import Activity
Activity.objects.all().delete()
activities = [
    'touching face', 
    'jotting',
    'clinking',
    'drinking(w/o handle)',
    'pulling out tissue',
    'drinking(w/ handle)',
    'eating w/ spoon',
    'eating w/ chopsticks',
    'eating w/ fork',
    'stirring',
    'idle',
    ]

for i,activity in enumerate(activities):
    Activity.objects.create(activity_label=activity,activity_id = i)
