"""Backfill is_bot and bot_type for existing records using browser_type and device_type."""

from django.db import migrations, models


# Map browser_type values (from ua-parser) to bot categories.
# Order matters: first match wins.
BOT_BROWSER_MAP = {
    'AI': [
        'Bytespider', 'GPTBot', 'ChatGPT-User', 'OAI-SearchBot',
        'ClaudeBot', 'Anthropic', 'CCBot', 'PetalBot', 'Amazonbot',
        'Diffbot', 'YouBot', 'AI2Bot', 'Cohere', 'PerplexityBot',
        'Meta-ExternalAgent', 'ImagesiftBot', 'img2dataset',
        'FriendlyCrawler',
    ],
    'SEO': [
        'AhrefsBot', 'SemrushBot', 'Semrush', 'MJ12bot', 'DotBot',
        'RogerBot', 'DataForSEO', 'ZoominfoBot', 'BLEXBot',
        'Screaming Frog', 'Serpstatbot', 'MegaIndex', 'Majestic',
        'LinkdexBot',
    ],
    'Search Engine': [
        'Googlebot', 'Googlebot-Image', 'Googlebot-Video',
        'Google-InspectionTool', 'Google-Extended', 'Storebot-Google',
        'Bingbot', 'BingPreview', 'Yahoo! Slurp', 'DuckDuckBot',
        'YandexBot', 'Yandex', 'Baiduspider', 'Sogou', 'Applebot',
        'NaverBot', 'Qwantify', 'Ecosia',
    ],
    'Social': [
        'facebookexternalhit', 'Facebot', 'Twitterbot', 'LinkedInBot',
        'WhatsApp', 'TelegramBot', 'Discordbot', 'Slackbot',
        'Pinterestbot', 'Redditbot',
    ],
    'Monitoring': [
        'Pingdom', 'UptimeRobot', 'StatusCake', 'Site24x7',
        'GTmetrix', 'Lighthouse', 'Google PageSpeed Insights',
        'NewRelicPinger', 'Datadog', 'PRTG',
    ],
    'Scraper': [
        'curl', 'Wget', 'HTTPie', 'httpx',
        'Python Requests', 'Python-urllib', 'python-httpx',
        'Go-http-client', 'Java', 'Apache-HttpClient',
        'node-fetch', 'Axios', 'undici',
        'Scrapy', 'Mechanize', 'Colly',
        'HeadlessChrome', 'PhantomJS',
        'Ruby', 'Perl', 'libwww-perl',
    ],
    'Archiver': [
        'ia_archiver', 'archive.org_bot', 'Heritrix', 'Wayback',
    ],
    'Feed': [
        'Feedly', 'NewsBlur', 'Inoreader', 'Feedbin',
        'SimplePie', 'FeedFetcher', 'Fever',
    ],
    'Validator': [
        'W3C_Validator', 'W3C_CSS_Validator', 'W3C-checklink',
    ],
}

# Build a reverse lookup: browser_type (lowercased) -> bot_type
_BROWSER_TO_BOT_TYPE = {}
for bot_type, browsers in BOT_BROWSER_MAP.items():
    for browser in browsers:
        _BROWSER_TO_BOT_TYPE[browser.lower()] = bot_type


def _classify(browser_type, device_type):
    """Return (is_bot, bot_type) based on stored browser_type and device_type."""
    bt_lower = (browser_type or '').lower()

    # Direct match on browser_type
    if bt_lower in _BROWSER_TO_BOT_TYPE:
        return True, _BROWSER_TO_BOT_TYPE[bt_lower]

    # Partial match for browser_type values that contain bot keywords
    for browser_key, bot_type in _BROWSER_TO_BOT_TYPE.items():
        if browser_key in bt_lower or bt_lower in browser_key:
            return True, bot_type

    # device_type "Spider" means ua-parser flagged it as a bot
    if (device_type or '').lower() == 'spider':
        return True, 'Other'

    return False, ''


def backfill_bot_type(apps, schema_editor):
    ActivityLog = apps.get_model('home', 'ActivityLog')
    WebEntry = apps.get_model('home', 'WebEntry')

    for Model in (ActivityLog, WebEntry):
        records = Model.objects.all().only('browser_type', 'device_type', 'is_bot', 'bot_type')
        to_update = []
        for record in records.iterator(chunk_size=1000):
            is_bot, bot_type = _classify(record.browser_type, record.device_type)
            if is_bot != record.is_bot or bot_type != record.bot_type:
                record.is_bot = is_bot
                record.bot_type = bot_type
                to_update.append(record)
            if len(to_update) >= 1000:
                Model.objects.bulk_update(to_update, ['is_bot', 'bot_type'])
                to_update = []
        if to_update:
            Model.objects.bulk_update(to_update, ['is_bot', 'bot_type'])


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_activitylog_bot_type_webentry_bot_type'),
    ]

    operations = [
        migrations.RunPython(backfill_bot_type, migrations.RunPython.noop),
    ]
