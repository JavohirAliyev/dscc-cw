"""
Django settings for Library Management System project.
"""
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library',  # Our main application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files
    'django.middleware.gzip.GZipMiddleware',  # Compress responses
    'django.middleware.http.ConditionalGetMiddleware',  # Support for conditional GET requests
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration with connection pooling
import sys

# Use SQLite for testing
if 'pytest' in sys.modules or 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    try:
        import dj_db_conn_pool  # noqa
        db_engine = 'dj_db_conn_pool.backends.postgresql'
        pool_options = {
            'POOL_OPTIONS': {
                'POOL_SIZE': 20,  # Increased pool size for better concurrency
                'MAX_OVERFLOW': 10,
                'POOL_RECYCLE': 3600,  # Recycle connections after 1 hour
                'POOL_PRE_PING': True,  # Check connection health before using
            }
        }
    except ImportError:
        # Fallback to standard PostgreSQL backend
        db_engine = 'django.db.backends.postgresql'
        pool_options = {}
    # Ensure a PostgreSQL DB adapter is available before using the postgres backend.
    # If none is installed and we're in DEBUG mode, fall back to a local SQLite file
    # to allow local development without installing `psycopg`/`psycopg2`.
    import importlib
    db_adapter_available = False
    try:
        importlib.import_module('psycopg')
        db_adapter_available = True
    except ImportError:
        try:
            importlib.import_module('psycopg2')
            db_adapter_available = True
        except ImportError:
            db_adapter_available = False

    if not db_adapter_available:
        if DEBUG:
            # Use a local SQLite file for development when Postgres adapter missing
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
        else:
            from django.core.exceptions import ImproperlyConfigured

            raise ImproperlyConfigured(
                'PostgreSQL adapter (psycopg or psycopg2) is not installed.'
            )
    else:
        DATABASES = {
            'default': {
                'ENGINE': db_engine,
                'NAME': config('DB_NAME', default='library_db'),
                'USER': config('DB_USER', default='library_user'),
                'PASSWORD': config('DB_PASSWORD', default='password'),
                'HOST': config('DB_HOST', default='localhost'),
                'PORT': config('DB_PORT', default='5432'),
                'CONN_MAX_AGE': 600,  # Keep connections alive for 10 minutes
                'CONN_HEALTH_CHECKS': True,  # Enable connection health checks
                'OPTIONS': {
                    'connect_timeout': 10,
                    'options': '-c statement_timeout=30000 -c lock_timeout=10000',  # Query and lock timeouts
                    'keepalives': 1,
                    'keepalives_idle': 30,
                    'keepalives_interval': 10,
                    'keepalives_count': 5,
                },
                **pool_options
            }
        }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout redirects
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# Cache configuration
REDIS_URL = config('REDIS_URL', default=None)

if REDIS_URL:
    # Use Redis for caching and sessions in production
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                    'retry_on_timeout': True,
                },
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
            },
            'KEY_PREFIX': 'library',
            'TIMEOUT': 300,  # 5 minutes default
        }
    }
    
    # Use Redis for session storage
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    # Fallback to local memory cache for development
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    
# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False  # Don't update session on every request

# Template optimization
if not DEBUG:
    # Cache templates in production
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
    TEMPLATES[0]['APP_DIRS'] = False  # Must be False when using cached loader

# Database query optimization
# Log slow queries in production for monitoring
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'WARNING',  # Only log slow queries and errors
                'propagate': False,
            },
        },
    }

# Security settings for production
if not DEBUG:
    # Trust Azure Container Apps proxy headers for HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Additional security headers
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True