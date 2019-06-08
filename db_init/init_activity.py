from contexts.models import Activity
Activity.objects.all().delete()
activities = [
    'touching\nface', 
    'jotting',
    'clinking',
    'drinking\n(w/o handle)',
    'pulling out\ntissue',
    'drinking\n(w/ handle)',
    'eating\n(w/ spoon)',
    'eating\n(w/ chopsticks)',
    'eating\n(w/ fork)',
    'stirring',
    'idle',
    ]

for i,activity in enumerate(activities):
    Activity.objects.create(activity_label=activity,activity_id = i)
