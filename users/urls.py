from django.urls import path

from .apps import UsersConfig
from . import views

app_name = UsersConfig.name


urlpatterns = [
    path('users/', views.UserTemplateView.as_view(), name='users')
]
