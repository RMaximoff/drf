from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    city = models.CharField(max_length=235, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватарка', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

