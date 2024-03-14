from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import ActivityLog, WebEntry
import requests
import json
from project.settings import DEBUG, BASE_DIR

import os
import geoip2.database

# IP Geolocation Database
url_asn = os.path.join(BASE_DIR, 'project/geoip/GeoLite2-ASN.mmdb')
reader_asn = geoip2.database.Reader(url_asn)

url_city = os.path.join(BASE_DIR, 'project/geoip/GeoLite2-City.mmdb')
reader_city = geoip2.database.Reader(url_city)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
  # LOGIKA UNTUK JENIS ELEKTRONIK
  if request.user_agent.is_mobile:
    electronic = 'Smartphone'
  elif request.user_agent.is_tablet:
    electronic = 'Tablet'
  elif request.user_agent.is_pc:
    electronic = 'PC/Laptop'
  else:
    electronic = None

  # LOGIKA UNTUK TIPE DEVICE
  if request.user_agent.device.family == None:
    device_type = 'None'
  else:
    device_type=request.user_agent.device.family

  # LOGIKA UNTUK BRAND DEVICE 
  if request.user_agent.device.brand == None:
    device_brand = 'None'
  else:
    device_brand=request.user_agent.device.brand

  # LOGIKA UNITUK MODEL DEVICE
  if request.user_agent.device.model == None:
    device_model = 'None'
  else:
    device_model=request.user_agent.device.model

  WebEntry.objects.create(
    action='User Login', 
    ip=request.META.get('REMOTE_ADDR'),
    electronic=electronic,
    is_touchscreen=request.user_agent.is_touch_capable,
    is_bot=request.user_agent.is_bot,
    os_type=request.user_agent.os.family,
    os_version=request.user_agent.os.version_string,
    browser_type=request.user_agent.browser.family,
    browser_version=request.user_agent.browser.version_string,
    device_type=device_type,
    device_brand=device_brand,
    device_model=device_model,
    username=user.username)

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
  creds = credentials

  # FETCH DATA GEOIP
  ip = request.META.get('REMOTE_ADDR')
  response_asn = reader_asn.asn(ip)
  response_city = reader_city.city(ip)
  
  # LOGIKA UNTUK JENIS ELEKTRONIK
  if request.user_agent.is_mobile:
    electronic = 'Smartphone'
  elif request.user_agent.is_tablet:
    electronic = 'Tablet'
  elif request.user_agent.is_pc:
    electronic = 'PC/Laptop'
  else:
    electronic = None

  # LOGIKA UNTUK TIPE DEVICE
  if request.user_agent.device.family == None:
    device_type = 'None'
  else:
    device_type=request.user_agent.device.family

  # LOGIKA UNTUK BRAND DEVICE 
  if request.user_agent.device.brand == None:
    device_brand = 'None'
  else:
    device_brand=request.user_agent.device.brand

  # LOGIKA UNITUK MODEL DEVICE
  if request.user_agent.device.model == None:
    device_model = 'None'
  else:
    device_model=request.user_agent.device.model

  WebEntry.objects.create(
    action='User Login Failed', 
    ip=ip,
    electronic=electronic,
    is_touchscreen=request.user_agent.is_touch_capable,
    is_bot=request.user_agent.is_bot,
    os_type=request.user_agent.os.family,
    os_version=request.user_agent.os.version_string,
    browser_type=request.user_agent.browser.family,
    browser_version=request.user_agent.browser.version_string,
    device_type=device_type,
    device_brand=device_brand,
    device_model=device_model,
    username=creds['username'],
    country_code=response_city.country.iso_code,
    country=response_city.country.names['en'],
    region_code=response_city.subdivisions[0].iso_code,
    region=response_city.subdivisions[0].names['en'],
    city=response_city.city.names['en'],
    lat=response_city.location.latitude,
    lon=response_city.location.longitude,
    timezone=response_city.location.time_zone,
    isp=response_asn.autonomous_system_organization)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
  if not DEBUG:
    # LOGIKA UNTUK JENIS ELEKTRONIK
    if request.user_agent.is_mobile:
      electronic = 'Smartphone'
    elif request.user_agent.is_tablet:
      electronic = 'Tablet'
    elif request.user_agent.is_pc:
      electronic = 'PC/Laptop'
    else:
      electronic = None

    # LOGIKA UNTUK TIPE DEVICE
    if request.user_agent.device.family == None:
      device_type = 'None'
    else:
      device_type=request.user_agent.device.family

    # LOGIKA UNTUK BRAND DEVICE 
    if request.user_agent.device.brand == None:
      device_brand = 'None'
    else:
      device_brand=request.user_agent.device.brand

    # LOGIKA UNITUK MODEL DEVICE
    if request.user_agent.device.model == None:
      device_model = 'None'
    else:
      device_model=request.user_agent.device.model

    WebEntry.objects.create(
      action='User Logout', 
      ip=request.META.get('REMOTE_ADDR'),
      electronic=electronic,
      is_touchscreen=request.user_agent.is_touch_capable,
      is_bot=request.user_agent.is_bot,
      os_type=request.user_agent.os.family,
      os_version=request.user_agent.os.version_string,
      browser_type=request.user_agent.browser.family,
      browser_version=request.user_agent.browser.version_string,
      device_type=device_type,
      device_brand=device_brand,
      device_model=device_model,
      username=user.username)

# LOGGING AKTIVITAS
def log_activity(request):
  ip = request.META.get('REMOTE_ADDR')
  if not DEBUG and ip != '127.0.0.1':
    # FETCH DATA GEOIP
    response_asn = reader_asn.asn(ip)
    response_city = reader_city.city(ip)

    # LOGIKA UNTUK JENIS ELEKTRONIK
    if request.user_agent.is_mobile:
      electronic = 'Smartphone'
    elif request.user_agent.is_tablet:
      electronic = 'Tablet'
    elif request.user_agent.is_pc:
      electronic = 'PC/Laptop'
    else:
      electronic = None

    # LOGIKA UNTUK TIPE DEVICE
    if request.user_agent.device.family == None:
      device_type = 'None'
    else:
      device_type=request.user_agent.device.family

    # LOGIKA UNTUK BRAND DEVICE 
    if request.user_agent.device.brand == None:
      device_brand = 'None'
    else:
      device_brand=request.user_agent.device.brand

    # LOGIKA UNITUK MODEL DEVICE
    if request.user_agent.device.model == None:
      device_model = 'None'
    else:
      device_model=request.user_agent.device.model

    # LOGIKA UNTUK USERNAME
    if request.user.is_authenticated:
      username = request.user.username
    else:
      username = 'User not login'

    activity = ActivityLog.objects.create(
      url_access=request.build_absolute_uri(), 
      ip=ip,
      electronic=electronic,
      is_touchscreen=request.user_agent.is_touch_capable,
      is_bot=request.user_agent.is_bot,
      os_type=request.user_agent.os.family,
      os_version=request.user_agent.os.version_string,
      browser_type=request.user_agent.browser.family,
      browser_version=request.user_agent.browser.version_string,
      device_type=device_type,
      device_brand=device_brand,
      device_model=device_model,
      username=username,
      country_code=response_city.country.iso_code,
      country=response_city.country.names['en'],
      region_code=response_city.subdivisions[0].iso_code,
      region=response_city.subdivisions[0].names['en'],
      city=response_city.city.names['en'],
      lat=response_city.location.latitude,
      lon=response_city.location.longitude,
      timezone=response_city.location.time_zone,
      isp=response_asn.autonomous_system_organization)
    return activity