from django.contrib import admin
from django.contrib.auth.models import User
from .models import Event,profile,Participant

# Register your models here.
admin.site.register(Event)
admin.site.register(profile)
admin.site.register(Participant)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_approved')
    list_filter = ('is_approved')
    actions = ['approve_providers']

    def approve_providers(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} provider(s) approved.")

def ready(self):
    import signals
