import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ('MANAGER', 'Manager'),
        ('MEMBER', 'Member'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
