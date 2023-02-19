from django.db import models
from django_better_admin_arrayfield.models import fields
from django.core.validators import RegexValidator

# Create your models here.
class Portfolio(models.Model):
  project_name = models.CharField(max_length=100)
  client_name = models.CharField(max_length=100)
  project_period = models.CharField(max_length=50)
  project_link = models.URLField()
  description = models.TextField()
  image = models.ImageField(upload_to='portfolio/', help_text='Rasio 1200px × 800px"')
  label = models.CharField(max_length=30)
  category = models.CharField(max_length=30)
  frameworks = fields.ArrayField(models.CharField(max_length=20), null=True, blank=True)

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

class ActivityLog(models.Model):
  url_access = models.URLField(editable=False)
  ip = models.GenericIPAddressField(null=True, editable=False)
  timestamp = models.DateTimeField(auto_now_add=True, editable=False)
  electronic = models.CharField(max_length=50, editable=False)
  is_touchscreen = models.BooleanField(editable=False)
  is_bot = models.BooleanField(editable=False)
  os_type = models.CharField(max_length=50, editable=False)
  os_version = models.CharField(max_length=50, editable=False)
  browser_type = models.CharField(max_length=50, editable=False)
  browser_version = models.CharField(max_length=50, editable=False)
  device_type = models.CharField(max_length=50, editable=False)
  device_brand = models.CharField(max_length=50, editable=False)
  device_model = models.CharField(max_length=50, editable=False)
  username = models.CharField(max_length=50, editable=False)

  # GEOIP
  country_code = models.CharField(max_length=5, editable=False, default='NONE')
  country = models.CharField(max_length=80, editable=False, default='None')
  region_code = models.CharField(max_length=5, editable=False, default='NONE')
  region = models.CharField(max_length=80, editable=False, default='None')
  city = models.CharField(max_length=80, editable=False, default='None')
  lat = models.DecimalField(max_digits= 8, decimal_places=4, editable=False, default=0.0)
  lon = models.DecimalField(max_digits= 8, decimal_places=4, editable=False, default=0.0)
  timezone = models.CharField(max_length=20, editable=False, default='None')
  isp = models.CharField(max_length=80, editable=False, default='None')
  isp_detail = models.CharField(max_length=100, editable=False, default='None')

class WebEntry(models.Model):
  class Meta:
    verbose_name_plural = 'Web entries'

  action = models.CharField(max_length=50, editable=False)
  ip = models.GenericIPAddressField(null=True, editable=False)
  timestamp = models.DateTimeField(auto_now_add=True, editable=False)
  electronic = models.CharField(max_length=50, editable=False)
  is_touchscreen = models.BooleanField(editable=False)
  is_bot = models.BooleanField(editable=False)
  os_type = models.CharField(max_length=50, editable=False)
  os_version = models.CharField(max_length=50, editable=False)
  browser_type = models.CharField(max_length=50, editable=False)
  browser_version = models.CharField(max_length=50, editable=False)
  device_type = models.CharField(max_length=50, editable=False)
  device_brand = models.CharField(max_length=50, editable=False)
  device_model = models.CharField(max_length=50, editable=False)
  username = models.CharField(max_length=50, editable=False)

  # GEOIP
  country_code = models.CharField(max_length=5, editable=False)
  country = models.CharField(max_length=80, editable=False)
  region_code = models.CharField(max_length=5, editable=False)
  region = models.CharField(max_length=80, editable=False)
  city = models.CharField(max_length=80, editable=False)
  lat = models.DecimalField(max_digits= 8, decimal_places=4, editable=False)
  lon = models.DecimalField(max_digits= 8, decimal_places=4, editable=False)
  timezone = models.CharField(max_length=20, editable=False)
  isp = models.CharField(max_length=80, editable=False)
  isp_detail = models.CharField(max_length=100, editable=False)