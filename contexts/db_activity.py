from contexts.models import Activity

activities = [
    'touching face', 
    'pouring',
    'raising hand',
    'using smartphone',
    'jotting',
    'clinking',
    'drinking (glass w/o handle)',
    'pulling out tissue',
    'drinking (glass w/ handle)',
    'eating with a spoon',
    'eating with chopsticks',
    'taking photo',
    'eating with a fork',
    'stirring',
    'using a keyboard',
    'using a mouse',
    ]

for activity in activities:
    Activity.objects.create(activity_label=activity)