from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, **extra_fields):
        """
        Create and save a user with the given phone.
        """
        if not phone:
            raise ValueError('The given phone must be set')

        user = self.model(phone=phone, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, phone, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, **extra_fields)

    def create_superuser(self, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, **extra_fields)
