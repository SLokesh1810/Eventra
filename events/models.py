from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=(('participant','Participant'),('provider','Provider'),))

    def __str__(self):
        return f"{self.user} ({self.role})"
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    mode = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')])
    location_or_link = models.CharField(max_length=255)
    provider = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to provider user
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_over = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.title} at {self.date_time}"
    
