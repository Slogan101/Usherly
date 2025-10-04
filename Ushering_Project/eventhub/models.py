import uuid
from django.db import models
from users.models import HostProfile
from django.utils import timezone
from utils.choices import EVENT_CHOICES, NIGERIAN_STATES, EVENT_MODES
from payment.models import Payment
from PIL import Image
# Create your models here.

class Events(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(HostProfile, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    event_image = models.ImageField(default='event-default.png', upload_to='event_banner', blank=True, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    state = models.CharField(max_length=20, choices=NIGERIAN_STATES)

    # Usher-specific fields (now optional)
    event_duration = models.PositiveBigIntegerField(blank=True, null=True)
    ushers_required = models.PositiveBigIntegerField(blank=True, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Common fields
    event_description = models.TextField(blank=True, null=True)
    event_mode = models.CharField(max_length=30, choices=EVENT_MODES, default='ushering_only')
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



class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="tickets")
    ticket_type = models.CharField(max_length=100)  # e.g., Regular, VIP
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_type} - {self.event.title}"
    


class TicketPurchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="purchases")
    buyer_name = models.CharField(max_length=255)
    buyer_email = models.EmailField()
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="ticket_purchase")
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.ticket.ticket_type} ({self.status})"