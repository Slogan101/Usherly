import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from .managers import CustomUserManager
from PIL import Image


# Create your models here.




class CustomUser(AbstractUser):
    USER_TYPES = (
        ('usher', 'Usher'),
        ('host', 'Host'),
    )
    username = None
    email = models.EmailField(unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    full_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.full_name} - {self.email}'



User = get_user_model()
class UsherProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usher_profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    phone = models.CharField(max_length=20)
    # size = models
    complexion = models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='usher_profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.full_name} - Usher'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)
    

class HostProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='host_profile')
    # organization = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.full_name} - Host'
    


