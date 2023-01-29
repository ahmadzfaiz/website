from django.contrib import admin
from .models import Experience, Skill

# Register your models here.
@admin.register(Experience)
class ExperienceModel(admin.ModelAdmin):
  list_display = ('id', 'workplace', 'position', 'period', 'label')

@admin.register(Skill)
class SkillModel(admin.ModelAdmin):
  list_display = ('id', 'name', 'label')