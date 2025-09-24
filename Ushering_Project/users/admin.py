from django.contrib import admin
from .models import CustomUser, UsherProfile, HostProfile

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(UsherProfile)
admin.site.register(HostProfile)