from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class User(models.Model):
    auth_token = models.CharField(
        help_text="Authorization token",
        max_length=32,
        validators=[MinLengthValidator(32)]
    )
    name = models.CharField(
        help_text="User's name",
        max_length=40,
        validators=[MinLengthValidator(4)]
    )
    email = models.EmailField(
        help_text="User's email",
    )
    meta = models.TextField(help_text="User's meta data", max_length=200)

    def __str__(self):
        return self.name
