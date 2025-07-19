from django.contrib import admin
from .models import Event, profile,Participant

# Register your models here.
admin.site.register(Event)
admin.site.register(profile)
admin.site.register(Participant)