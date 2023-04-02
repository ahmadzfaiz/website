from django.urls import path
from .views import home, article, article_post, register

urlpatterns = [
  path('blog', home, name='blog'),
  path('blog/article', article, name='article'),
  path('blog/article/<int:pk>/', article_post, name='article_post'),

  # Account
  path('accounts/register', register, name='register'),
]