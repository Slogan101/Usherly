import uuid
from django.db import models
from users.models import HostProfile
from django.utils import timezone
from utils.choices import EVENT_CHOICES, NIGERIAN_STATES
from PIL import Image
# Create your models here.

class Events(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(HostProfile, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    event_image = models.ImageField(default='event-default.png', upload_to='event_banner', blank=True, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    state = models.CharField(max_length=20, choices=NIGERIAN_STATES)
    event_duration = models.PositiveBigIntegerField()
    event_description = models.TextField(blank=True, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} by {self.host.user.full_name}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.event_image:
            img = Image.open(self.event_image.path)
            banner_size = (600, 300)
            img = img.resize(banner_size, Image.Resampling.LANCZOS)
            img.save(self.event_image.path)