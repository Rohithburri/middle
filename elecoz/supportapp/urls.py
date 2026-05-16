from django.urls import path
from .views import create_support

urlpatterns = [
    path('support/', create_support),
]