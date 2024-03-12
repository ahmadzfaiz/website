from django.contrib import admin
from .models import post
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

# Register your models here.
@admin.register(post)
class postAdmin(admin.ModelAdmin, DynamicArrayMixin):
  list_display = ('title', 'author', 'updated_at')