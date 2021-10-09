from django.contrib.auth import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    author = models.BooleanField(default=False, blank=True)