from django.contrib import admin

from .models import Plant, ScheduledPlant

admin.site.register(Plant)
admin.site.register(ScheduledPlant)
