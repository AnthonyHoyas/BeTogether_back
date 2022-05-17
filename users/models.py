from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
# import polls.models


class CustomUser(AbstractUser):
    
    petitsurnommigion = models.CharField(max_length=128, default= 'If youre seeing this, youre cute')
    is_coach = models.BooleanField(default=False)
    date_of_birth = models.DateField(default=date.today)
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    promotion = models.ForeignKey('polls.Promotion', blank=True, null=True, on_delete=models.CASCADE)
    

    REQUIRED_FIELDS = ['is_coach', 'email']

    class Meta:
        db_table = 'auth_user'
    
    def __str__(self):
        return self.username