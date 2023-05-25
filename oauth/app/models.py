import uuid

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from oauth2_provider.models import AbstractApplication


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    username = models.CharField(_("username"),
                                max_length=150, help_text=_(
        "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    ), null=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    phone = models.CharField(max_length=15, null=True, default=None, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [""]


# TODO custom application table

class Applicaiton(AbstractApplication):
    def allows_grant_type(self, *grant_types):
        return bool(set([self.authorization_grant_type, self.GRANT_CLIENT_CREDENTIALS, self.GRANT_PASSWORD]) & grant_types)
