from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.conf import settings
from .models import ActivityLog, WebEntry

import ipaddress
import logging
import os
import geoip2.database

logger = logging.getLogger(__name__)

# GeoIP database directory (bind-mounted, updated externally by Prefect)
GEOIP_DIR = os.path.join(settings.BASE_DIR, 'project/geoip')
ASN_PATH = os.path.join(GEOIP_DIR, 'GeoLite2-ASN.mmdb')
CITY_PATH = os.path.join(GEOIP_DIR, 'GeoLite2-City.mmdb')

reader_asn = None
reader_city = None
_last_mtime_asn = 0
_last_mtime_city = 0


def _load_geoip_readers():
    """Load or reload GeoIP readers if files are new or changed."""
    global reader_asn, reader_city, _last_mtime_asn, _last_mtime_city
    changed = False

    try:
        if os.path.exists(ASN_PATH):
            mtime = os.path.getmtime(ASN_PATH)
            if mtime != _last_mtime_asn:
                if reader_asn:
                    reader_asn.close()
                reader_asn = geoip2.database.Reader(ASN_PATH)
                _last_mtime_asn = mtime
                changed = True
        else:
            reader_asn = None

        if os.path.exists(CITY_PATH):
            mtime = os.path.getmtime(CITY_PATH)
            if mtime != _last_mtime_city:
                if reader_city:
                    reader_city.close()
                reader_city = geoip2.database.Reader(CITY_PATH)
                _last_mtime_city = mtime
                changed = True
        else:
            reader_city = None

        if changed:
            logger.info('GeoIP databases reloaded')
    except Exception as e:
        logger.warning('Failed to load GeoIP databases: %s', e)


# Load on startup if files exist
_load_geoip_readers()


def get_client_ip(request):
    """Get real client IP, preferring CF-Connecting-IP from Cloudflare."""
    return (
        request.META.get('HTTP_CF_CONNECTING_IP')
        or request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
        or request.META.get('REMOTE_ADDR')
    )


def is_public_ip(ip):
    """Check if an IP is public (not private/loopback/reserved)."""
    try:
        return ipaddress.ip_address(ip).is_global
    except (ValueError, TypeError):
        return False


def get_geoip_data(ip):
    """Lookup GeoIP data, auto-reloads if mmdb files changed on disk."""
    if not is_public_ip(ip):
        return None

    _load_geoip_readers()

    if not reader_city or not reader_asn:
        return None
    try:
        city = reader_city.city(ip)
        asn = reader_asn.asn(ip)
        return {
            'country_code': city.country.iso_code or 'NONE',
            'country': city.country.names.get('en', 'None'),
            'region_code': city.subdivisions[0].iso_code if city.subdivisions else 'NONE',
            'region': city.subdivisions[0].names.get('en', 'None') if city.subdivisions else 'None',
            'city': city.city.names.get('en', 'None') if city.city.names else 'None',
            'lat': city.location.latitude or 0.0,
            'lon': city.location.longitude or 0.0,
            'timezone': city.location.time_zone or 'None',
            'isp': asn.autonomous_system_organization or 'None',
        }
    except Exception as e:
        logger.warning('GeoIP lookup failed for %s: %s', ip, e)
        return None


def get_device_info(request):
    """Extract device info from user agent."""
    if request.user_agent.is_mobile:
        electronic = 'Smartphone'
    elif request.user_agent.is_tablet:
        electronic = 'Tablet'
    elif request.user_agent.is_pc:
        electronic = 'PC/Laptop'
    else:
        electronic = 'None'

    return {
        'electronic': electronic,
        'is_touchscreen': request.user_agent.is_touch_capable,
        'is_bot': request.user_agent.is_bot,
        'os_type': request.user_agent.os.family,
        'os_version': request.user_agent.os.version_string,
        'browser_type': request.user_agent.browser.family,
        'browser_version': request.user_agent.browser.version_string,
        'device_type': request.user_agent.device.family or 'None',
        'device_brand': request.user_agent.device.brand or 'None',
        'device_model': request.user_agent.device.model or 'None',
    }


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    device = get_device_info(request)
    geo = get_geoip_data(ip) or {}

    WebEntry.objects.create(
        action='User Login',
        ip=ip,
        username=user.username,
        **device,
        **geo,
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    device = get_device_info(request)
    geo = get_geoip_data(ip) or {}

    WebEntry.objects.create(
        action='User Login Failed',
        ip=ip,
        username=credentials.get('username', 'Unknown'),
        **device,
        **geo,
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    device = get_device_info(request)

    WebEntry.objects.create(
        action='User Logout',
        ip=ip,
        username=user.username,
        **device,
    )


def log_activity(request):
    ip = get_client_ip(request)
    if not is_public_ip(ip):
        return None

    device = get_device_info(request)
    geo = get_geoip_data(ip) or {}

    username = request.user.username if request.user.is_authenticated else 'User not login'

    return ActivityLog.objects.create(
        url_access=request.build_absolute_uri(),
        ip=ip,
        username=username,
        **device,
        **geo,
    )
