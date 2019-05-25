from django.contrib import admin

# Register your models here.
from .models import FeatureRecord, RawDataRecord, ActivityInferenceRecord
admin.site.register(FeatureRecord)
admin.site.register(RawDataRecord)
admin.site.register(ActivityInferenceRecord)