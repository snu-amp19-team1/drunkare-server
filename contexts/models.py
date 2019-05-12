from django.db import models

# Create your models here.
class Context(models.Model):
    context_id = models.AutoField(primary_key=True)
    context_label = models.CharField(max_length=100)
    
    class Meta:
        managed = True

    def __str__(self):
        return str(self.context_label)

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_label = models.CharField(max_length=100)
    
    class Meta:
        managed = True

    def __str__(self):
        return str(self.activity_label)