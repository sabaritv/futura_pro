from django.contrib import admin
from data_app import models
# Register your models here.


admin.site.register(models.Login)
admin.site.register(models.Receiver)
admin.site.register(models.Owner)
admin.site.register(models.Uploads)