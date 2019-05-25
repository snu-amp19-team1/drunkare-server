from data.models import RawDataRecord,FeatureRecord,ActivityInferenceRecord

ActivityInferenceRecord.objects.all().delete()
FeatureRecord.objects.all().delete()
RawDataRecord.objects.all().delete()