from django.contrib.auth.models import AbstractUser
from django.contrib.admin import display
from django.contrib.auth import models
from django.utils import timezone
from django.db import models

# Create your models here.

class User(AbstractUser):
    author = models.BooleanField(default=False, blank=True)
    special_user = models.DateTimeField(default=timezone.now, verbose_name='Special User')

    @display(
        boolean=True,
        description="Special User",
    )
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False


