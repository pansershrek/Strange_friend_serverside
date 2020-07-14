from django.urls import path
from authorization_app.views.views import *

urlpatterns = [
    path('create_user', create_user, name='create_user'),
    path('change_settings', change_settings, name='change_settings'),
    path('post_data', post_data, name='post_data'),
    path('validate_user', validate_user, name='validate_user'),
    path('match_data', match_data, name='match_data')
]
