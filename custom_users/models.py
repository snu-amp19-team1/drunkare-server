from django.db import models
from contexts.models import Context
# Create your models here.
class CustomUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100)
    recent_activities = models.CharField(max_length=100, blank=True,)
    current_location = models.CharField(max_length=100, blank=True)
    current_context = models.ForeignKey(Context,models.DO_NOTHING, null=True,blank=True,)
    last_update = models.DateTimeField(null=True,blank=True,)

    class Meta:
        managed = True

    def __str__(self):
        return str(self.user_name)