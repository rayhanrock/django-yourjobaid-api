from django.contrib import admin
from YourJobAidApi import models

admin.site.register(models.UserProfile)
admin.site.register(models.Category)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.ContactUs)
