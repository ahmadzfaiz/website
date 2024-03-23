from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomeView

urlpatterns = [
  path('', HomeView.as_view(), name='gempa_home'),
]