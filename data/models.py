from django.db import models

# Create your models here.
class RawDataRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    data_type = models.IntegerField(blank=True,default=0)
    x = models.TextField(blank=True,default='')
    y = models.TextField(blank=True,default='')
    z = models.TextField(blank=True,default='')
    
    class Meta:
        managed = True
    
    def __str__(self):
        return str(self.timestamp)

class FeatureRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    window_mean = models.FloatField()
    window_stddev = models.FloatField()
    window_median = models.FloatField()
    window_percent25 = models.FloatField()
    window_percent75 = models.FloatField()

    class Meta:
        managed = True

    def __str__(self):
        return str(self.timestamp)