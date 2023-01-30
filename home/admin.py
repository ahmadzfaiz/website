from django.contrib import admin
from django import forms
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import Portfolio, Experience, Certificate, Skill, Contact

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