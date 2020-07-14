from django.db import models
from authorization_app.models.user import User

# Create your models here.


class DataOwnership(models.Model):
    id_owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        help_text="This data belongs to"
    )
    id_data_value = models.TextField(help_text="Owned data's id")
    data_type = models.TextField(help_text="Data type")
    timestamp = models.BigIntegerField(help_text="Data store timestamp")

    def __str__(self):
        return self.id_data_value
