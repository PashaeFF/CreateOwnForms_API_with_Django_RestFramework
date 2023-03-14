from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import jwt


class User(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=500)
    company = models.BooleanField(default=True)
    last_login = models.DateTimeField(default=now())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []