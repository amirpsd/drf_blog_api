from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.admin import display
from django.utils import timezone
from django.db import models

from .managers import CustomUserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    )
    phone = models.CharField(
        max_length=11,
        validators=[phone_regex],
        unique=True,
        verbose_name=_("phone")
    )
    first_name = models.CharField(max_length=100, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=100, blank=True, verbose_name=_('last name'))
    author = models.BooleanField(default=False, blank=True, verbose_name=_("author"))
    special_user = models.DateTimeField(default=timezone.now, verbose_name=_('Special User'))

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    @property
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    @display(
        boolean=True,
        description="Special User",
    )
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
