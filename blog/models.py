from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django_better_admin_arrayfield.models.fields import ArrayField

# Create your models here.
class post(models.Model):
  title = models.CharField(max_length=50)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  tags = ArrayField(models.CharField(max_length=30), null=True, blank=True)
  body = RichTextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)