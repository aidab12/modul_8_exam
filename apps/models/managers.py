from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_active", False)
        if not phone:
            raise ValueError('Phone must be provided')

        user = self.model(phone=phone, **extra_fields)
        if password:
            user.password = make_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user



    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)