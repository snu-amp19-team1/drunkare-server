#drink 0, eat 1, cafe 2, desk 3
from contexts.models import Context

contexts = [
    'drinking',
    'eating',
    'at a cafe',
    'at a desk',
    ]

for i,context in enumerate(contexts):
    Context.objects.create(context_label=context,context_id = i)