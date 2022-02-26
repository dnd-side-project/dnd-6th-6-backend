from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Profile, models.EmailAuth)
class UserAdmin(admin.ModelAdmin):
    pass
