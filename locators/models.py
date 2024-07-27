from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=10)
    serviceProviding = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'phoneNumber', 'serviceProviding']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class LatLong(models.Model):
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}, User: {self.user.username}"


