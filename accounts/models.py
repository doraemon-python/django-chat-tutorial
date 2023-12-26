from django.db import models
from django.utils.crypto import get_random_string

import uuid


class UserManager(models.Manager):
    def create_user(self, email):
        while True:
            username = "ユーザー#" + get_random_string(
                5,
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            )
            if not self.filter(username=username).exists():
                break
        return self.create(username=username, email=email)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    is_active = True

    objects = UserManager()

    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
