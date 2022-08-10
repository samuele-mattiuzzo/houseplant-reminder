from django.contrib import admin

from .models import ScheduledTask, Task

admin.site.register(Task)
admin.site.register(ScheduledTask)
