from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='آدرس ایمیل',
        max_length=255,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        verbose_name='شماره تلفن',
        unique=True,
        max_length=12
    )
    age = models.IntegerField(
        verbose_name='سن',
        blank=True,
        null=True
    )
    profile_photo = models.ImageField(
        verbose_name='عکس پروفایل',
        upload_to='media/images/profiles',
        default='None.png',
        blank=True,
        null=True
    )
    about_me = models.TextField(
        verbose_name='درباره',
        max_length=250,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.first_name or self.last_name:
            return self.get_full_name()
        else:
            return self.phone_number


class OTP(models.Model):
    token = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=11)
    password = models.CharField(max_length=60, null=True)
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)
