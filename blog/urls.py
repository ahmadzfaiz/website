from django.urls import path
from .views import blog, register
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView

urlpatterns = [
  path('blog', blog, name='blog'),

  # Account
  path('accounts/register', register, name='register'),
]