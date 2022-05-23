from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class CustomUser(AbstractUser):
    petitsurnommigion = models.CharField(max_length=128, default= 'If youre seeing this, youre cute')
    is_coach = models.BooleanField(default=False)
    date_of_birth = models.DateField(default=date.today)
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    promotion = models.ForeignKey('polls.Promotion', blank=True, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, blank=True, null=True, default='' )
    email = models.EmailField(('email'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # REQUIRED_FIELDS = ['is_coach', 'email']

    class Meta:
        db_table = 'auth_user'
    
    def __str__(self):
        return self.email

  
