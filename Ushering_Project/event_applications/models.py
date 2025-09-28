import uuid
from django.db import models
from users.models import UsherProfile
from eventhub.models import Events
from utils.choices import STATUS_CHOICES
from django.utils import timezone

# Create your models here.



class ApplicationManager(models.Manager):
    def pending(self):
        return self.filter(status='pending')
    
    def rejected(self):
        return self.filter(status='rejected')

    def accepted(self):
        return self.filter(status='accepted')




class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usher = models.ForeignKey(UsherProfile, on_delete=models.CASCADE, related_name="applications")
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(default=timezone.now)

    objects = ApplicationManager()

    def __str__(self):
        return f"{self.usher.user.username} → {self.event.title} ({self.status})"
    

    def update_status(self, new_status):
        if new_status not in dict(STATUS_CHOICES):
            raise ValueError("Invalid status")
        self.status = new_status
        self.save()
