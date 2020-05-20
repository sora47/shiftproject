from django.contrib import admin
from .models import ShiftBaseModel, ShiftModel

# Register your models here.

admin.site.register(ShiftBaseModel)
admin.site.register(ShiftModel)