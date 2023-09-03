from django.contrib import admin

from . import models

admin.site.register(models.student)
admin.site.register(models.subject)
admin.site.register(models.faculty)
admin.site.register(models.attendance)