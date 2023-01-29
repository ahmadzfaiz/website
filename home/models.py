from django.db import models

# Create your models here.
class Experience(models.Model):
  workplace = models.CharField(max_length=50)
  position = models.CharField(max_length=30)
  period = models.CharField(max_length=50)
  image = models.ImageField(upload_to='experience/', help_text="Rasio harus persegi. Contoh: 600px × 600px")
  label = models.CharField(max_length=30)
  description = models.TextField()

class Skill(models.Model):
  name = models.CharField(max_length=20)
  image = models.ImageField(upload_to='skills/')
  reference = models.URLField()
  label = models.CharField(max_length=30)