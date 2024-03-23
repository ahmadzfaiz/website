from django.urls import path
from .views import home, article, article_post, register

urlpatterns = [
  path('', home, name='blog'),
  path('article', article, name='article'),
  path('article/<int:pk>/', article_post, name='article_post'),

  # Account
  path('accounts/register', register, name='register'),
]