from django.db import models

# Create your models here.
# class RawData(model.Model):
#   don't implement for now, write to file and extract features directly

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