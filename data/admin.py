from django.contrib import admin

# Register your models here.
from .models import FeatureRecord, RawDataRecord
admin.site.register(FeatureRecord)
admin.site.register(RawDataRecord)