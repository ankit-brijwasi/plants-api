from django.contrib.auth.models import AbstractUser
from django.db import models

USER_TYPE = (
    ('user', 'user'),
    ('nursury', 'nursury'),
)

class User(AbstractUser):
    type = models.CharField(max_length=10, choices=USER_TYPE, default='user')

    def __str__(self):
        return self.username