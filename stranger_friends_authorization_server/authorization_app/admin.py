from django.contrib import admin
from authorization_app.models.user import User
from authorization_app.models.data_ownership import DataOwnership

# Register your models here.

admin.site.register(User)
admin.site.register(DataOwnership)
