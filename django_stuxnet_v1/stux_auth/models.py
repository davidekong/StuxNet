from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, default="xxxxxxxxxxxxxxx")
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

class OneTimePassword(models.Model):
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.CharField(max_length=100)
    type = models.IntegerField(max_length=2, default=0)
