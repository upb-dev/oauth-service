from django.db import models
import uuid

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, null=True, default=None, blank=True)