from django.db import models

# Create your models here.
class RawDataRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    X_acc = models.CharField(max_length=1000)
    Y_acc = models.CharField(max_length=1000)
    Z_acc = models.CharField(max_length=1000)
    X_gyro = models.CharField(max_length=1000)
    Y_gyro = models.CharField(max_length=1000)
    Z_gyro = models.CharField(max_length=1000)

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