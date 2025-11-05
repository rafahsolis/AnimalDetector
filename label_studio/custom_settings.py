"""
Custom Django settings for Label Studio to fix CSRF issues behind Cloudflare tunnel
"""

CSRF_TRUSTED_ORIGINS = [
    'https://label.montedelavilla.org',
]

ALLOWED_HOSTS = [
    'label.montedelavilla.org',
    'localhost',
    '127.0.0.1',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_DOMAIN = 'label.montedelavilla.org'
