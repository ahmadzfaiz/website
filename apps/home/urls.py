from django.urls import path
from .views import home, pegadaian_api

urlpatterns = [
  path('', home, name='home'),
]