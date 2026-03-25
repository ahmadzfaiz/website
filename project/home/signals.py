from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.conf import settings
from .models import ActivityLog, WebEntry

import os
import geoip2.database

# IP Geolocation Database
url_asn = os.path.join(settings.BASE_DIR, 'project/geoip/GeoLite2-ASN.mmdb')
reader_asn = geoip2.database.Reader(url_asn)

url_city = os.path.join(settings.BASE_DIR, 'project/geoip/GeoLite2-City.mmdb')
reader_city = geoip2.database.Reader(url_city)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if request.user_agent.is_mobile:
        electronic = 'Smartphone'
    elif request.user_agent.is_tablet:
        electronic = 'Tablet'
    elif request.user_agent.is_pc:
        electronic = 'PC/Laptop'
    else:
        electronic = None

    device_type = request.user_agent.device.family or 'None'
    device_brand = request.user_agent.device.brand or 'None'
    device_model = request.user_agent.device.model or 'None'

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
        username=user.username,
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    response_asn = reader_asn.asn(ip)
    response_city = reader_city.city(ip)

    if request.user_agent.is_mobile:
        electronic = 'Smartphone'
    elif request.user_agent.is_tablet:
        electronic = 'Tablet'
    elif request.user_agent.is_pc:
        electronic = 'PC/Laptop'
    else:
        electronic = None

    device_type = request.user_agent.device.family or 'None'
    device_brand = request.user_agent.device.brand or 'None'
    device_model = request.user_agent.device.model or 'None'

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
        username=credentials['username'],
        country_code=response_city.country.iso_code,
        country=response_city.country.names['en'],
        region_code=response_city.subdivisions[0].iso_code,
        region=response_city.subdivisions[0].names['en'],
        city=response_city.city.names['en'],
        lat=response_city.location.latitude,
        lon=response_city.location.longitude,
        timezone=response_city.location.time_zone,
        isp=response_asn.autonomous_system_organization,
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if not settings.DEBUG:
        if request.user_agent.is_mobile:
            electronic = 'Smartphone'
        elif request.user_agent.is_tablet:
            electronic = 'Tablet'
        elif request.user_agent.is_pc:
            electronic = 'PC/Laptop'
        else:
            electronic = None

        device_type = request.user_agent.device.family or 'None'
        device_brand = request.user_agent.device.brand or 'None'
        device_model = request.user_agent.device.model or 'None'

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
            username=user.username,
        )


def log_activity(request):
    ip = request.META.get('REMOTE_ADDR')
    if not settings.DEBUG and ip != '127.0.0.1':
        response_asn = reader_asn.asn(ip)
        response_city = reader_city.city(ip)

        if request.user_agent.is_mobile:
            electronic = 'Smartphone'
        elif request.user_agent.is_tablet:
            electronic = 'Tablet'
        elif request.user_agent.is_pc:
            electronic = 'PC/Laptop'
        else:
            electronic = None

        device_type = request.user_agent.device.family or 'None'
        device_brand = request.user_agent.device.brand or 'None'
        device_model = request.user_agent.device.model or 'None'

        username = request.user.username if request.user.is_authenticated else 'User not login'

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
            isp=response_asn.autonomous_system_organization,
        )
        return activity
