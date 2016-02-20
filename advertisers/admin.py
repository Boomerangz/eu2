__author__ = 'igor'

from django.contrib import admin

# Register your models here.

from .models import Banner, Campaign

admin.site.register(Banner)
admin.site.register(Campaign)
