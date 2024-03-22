from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import MainView, DetailView, HomeView

urlpatterns = [
  path('', HomeView.as_view(), name='cuaca_home'),
  path('<int:index>/', login_required(MainView.as_view()), name='cuaca_main'),
  path('<int:index1>/<int:index2>/', login_required(DetailView.as_view()), name='cuaca_detail'),
]