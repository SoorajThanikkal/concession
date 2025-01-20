from django.contrib import admin
from .import models
admin.site.register(models.user)
admin.site.register(models.Feedback)
admin.site.register(models.rto)
admin.site.register(models.Wallet)
admin.site.register(models.BusRoute)
admin.site.register(models.BusPass)
admin.site.register(models.Transaction)

# Register your models here.
