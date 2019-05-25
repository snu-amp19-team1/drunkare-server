from django.db import models

# Create your models here.
class RawDataRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    data_type = models.IntegerField(blank=True,default=0)
    x = models.TextField(blank=True,default='')
    y = models.TextField(blank=True,default='')
    z = models.TextField(blank=True,default='')
    user_id = models.IntegerField(blank=True,default=0)
    index = models.IntegerField(blank=True,default=0)

    class Meta:
        managed = True
    
    def __str__(self):
        return str(self.timestamp)

class FeatureRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    feature = models.CharField(max_length=1000,default='')
    user_id = models.IntegerField(blank=True,default=0)

    class Meta:
        managed = True

    def __str__(self):
        return str(self.record_id)


class ActivityRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    activity = models.CharField(max_length=1000,default='')
    user_id = models.IntegerField(blank=True,default=0)
    
    class Meta:
        managed = True

    def __str__(self):
        return str(self.record_id)