from django.contrib import admin

# Register your models here.

from .models import User, Report

admin.site.register(User)
admin.site.register(Report)
