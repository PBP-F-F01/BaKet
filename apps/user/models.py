from django.db import models
from datetime import datetime
# Create your models here.

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_image/', 
                                        default='profile_image/default.png',
                                        null=True, blank=True)
    
    birth_date = models.DateField(default=datetime(2000,1,1))
    gender = models.CharField(max_length=10, choices=[('Pria', 'Pria'), ('Wanita', 'Wanita')], null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"