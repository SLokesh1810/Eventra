from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=(('participant','Participant'),('organiser','Organiser'),('admin','Admin')))
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} ({self.role})"
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    timeAlloted = models.IntegerField(default=60)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    mode = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')])
    location_or_link = models.CharField(max_length=255)
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - Approved: {self.is_approved}"
    
class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')

    def __str__(self):
        return f"regId:{self.id} {self.user.username} → {self.event.title}"
    
class organizersWaiting(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Waiting: {self.user.username} for {self.event.title}"
