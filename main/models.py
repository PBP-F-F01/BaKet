from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_image/', 
                                        default='profile_image/default.png',
                                        null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"