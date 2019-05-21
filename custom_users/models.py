from django.db import models
from contexts.models import Activity,Context
# Create your models here.
class CustomUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100)
    current_activity = models.ForeignKey(Activity,models.DO_NOTHING, null=True,)
    current_context = models.ForeignKey(Context,models.DO_NOTHING, null=True,)

    class Meta:
        managed = True

    def __str__(self):
        return str(self.user_name)