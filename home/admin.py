from django.contrib import admin
from .models import Experience, Certificate, Skill, Contact

# Register your models here.
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