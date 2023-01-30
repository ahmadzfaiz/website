from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Experience(models.Model):
  workplace = models.CharField(max_length=50)
  position = models.CharField(max_length=30)
  period = models.CharField(max_length=50)
  image = models.ImageField(upload_to='experience/', help_text="Rasio harus persegi. Contoh: 600px × 600px")
  label = models.CharField(max_length=30)
  description = models.TextField()

class Certificate(models.Model):
  name = models.CharField(max_length=100)
  publisher = models.CharField(max_length=80)
  image = models.ImageField(upload_to='certificate/', help_text="Rasio harus persegi. Contoh: 600px × 600px")
  image_label = models.CharField(max_length=50)
  certificate_link = models.URLField()
  certificate_label = models.CharField(max_length=50)
  info_link = models.URLField()
  info_label = models.CharField(max_length=50)

class Skill(models.Model):
  name = models.CharField(max_length=20)
  image = models.ImageField(upload_to='skills/')
  reference = models.URLField()
  label = models.CharField(max_length=30)

class Contact(models.Model):
  name = models.CharField(max_length=50)
  email = models.EmailField()
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+6281255555555'. Up to 15 digits allowed.")
  phone_number = models.CharField(max_length=17, validators=[phone_regex])
  message = models.TextField()