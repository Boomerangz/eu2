__author__ = 'igor'

from django.contrib import admin

# Register your models here.

from .models import AdSpot, Site, Format, Theme

admin.site.register(AdSpot)
admin.site.register(Site)
admin.site.register(Format)
admin.site.register(Theme)
