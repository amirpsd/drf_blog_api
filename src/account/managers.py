from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone):
        if not phone:
            raise ValueError("User must have a phone number")

        user = self.model(phone=phone)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        if not phone:
            raise ValueError("Super User must have a phone number")

        if not password:
            raise ValueError("Super User must have a password")

        user = self.model(phone=phone)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
