# Python Imports
import uuid

# Django Imports
from django.contrib.auth.models import AbstractUser
from django.db import models

# Utils Import
from spotcloud_test.utils.BaseModel import BaseModel


# Create your models here.

class User(BaseModel, AbstractUser):
    unique_code = models.UUIDField('Code Unique Generate', default=uuid.uuid4, editable=False)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('First Name', max_length=255, blank=False, null=False)
    last_name = models.CharField('Last Name', max_length=255, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
