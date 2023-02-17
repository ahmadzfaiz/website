from django.contrib import admin
from django import forms
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import Portfolio, Experience, Certificate, Skill, Contact, ActivityLog, WebEntry

# Register your models here.    
@admin.register(Portfolio)
class PortfolioModel(admin.ModelAdmin, DynamicArrayMixin):
  list_display = ('id', 'project_name', 'client_name', 'project_period')

@admin.register(Experience)
class ExperienceModel(admin.ModelAdmin):
  list_display = ('id', 'workplace', 'position', 'period', 'label')

@admin.register(Certificate)
class CertificateModel(admin.ModelAdmin):
  list_display = ('id', 'name', 'publisher', 'certificate_link')

@admin.register(Skill)
class SkillModel(admin.ModelAdmin):
  list_display = ('id', 'name', 'label')

@admin.register(Contact)
class ContactModel(admin.ModelAdmin):
  list_display = ('id', 'name', 'email', 'phone_number')

@admin.register(ActivityLog)
class ActivityLogModel(admin.ModelAdmin):
  search_fields = ('username',)
  list_display = ('id', 'url_access', 'ip', 'electronic', 'browser_type', 'timestamp', 'username')
  list_filter = (
    'ip', 'url_access', 'timestamp', 'electronic', 
    'os_type', 'os_version', 'browser_type', 'browser_version', 
    'device_type', 'device_brand', 'device_model', 'username')

@admin.register(WebEntry)
class WebEntryModel(admin.ModelAdmin):
  search_fields = ('username',)
  list_display = ('id', 'ip', 'electronic', 'browser_type', 'action', 'timestamp', 'username')
  list_filter = (
    'ip', 'action', 'timestamp', 'electronic', 
    'os_type', 'os_version', 'browser_type', 'browser_version', 
    'device_type', 'device_brand', 'device_model', 'username')