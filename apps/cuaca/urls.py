from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import MainView, HomeView

urlpatterns = [
  path('<int:index>/', login_required(MainView.as_view()), name='cuaca_main'),
  path('', HomeView.as_view(), name='cuaca_home'),
]