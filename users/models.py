from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('ADMINISTRATOR', 'Administrator'),
        ('USER', 'User'),
    ]

    COMMUNICATION_CHANNEL_CHOICES = [
        ('POST', 'Pošta'),
        ('EMAIL', 'Email'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    communication_channel = models.CharField(max_length=10, choices=COMMUNICATION_CHANNEL_CHOICES, default='EMAIL')

    def __str__(self):
        return f'{self.user.username} Profile'
