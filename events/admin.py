from django.contrib import admin
from .models import Event,profile,Registration

# Register your models here.
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(profile)