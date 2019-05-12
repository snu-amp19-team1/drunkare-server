from django.contrib import admin

# Register your models here.
from .models import Context,Activity
admin.site.register(Context)
admin.site.register(Activity)