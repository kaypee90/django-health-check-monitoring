"""
Example Django settings for production environment with Django Health Check Monitoring.

This configuration syncs health check data to an external monitoring server
without local persistence to minimize database load.
"""

# Basic Django settings (you'll have more of these in your actual settings.py)
DEBUG = False
ALLOWED_HOSTS = ['example.com', 'www.example.com']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'production_db',
        'USER': 'db_user',
        'PASSWORD': 'secure_password',
        'HOST': 'db.example.com',
        'PORT': '5432',
    }
}

# Installed apps including health check monitoring
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Health check apps
    'django_health_check_job',
    'health_check',
    'health_check.db',                      # Database health check
    'health_check.cache',                   # Cache health check
    'health_check.storage',                 # Storage health check
    'health_check.contrib.migrations',      # Migrations health check
    'health_check.contrib.redis',           # Redis health check
    'health_check.contrib.celery',          # Celery health check
    'health_check.contrib.psutil',          # System resources check
]

# Cache configuration (Redis in production)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}

# ============================================================================
# Django Health Check Monitoring Configuration
# ============================================================================

# Disable database persistence in production to reduce DB load
PERSIST_HEALTH_CHECK_DATA = False

# Enable syncing to external monitoring server
SYNC_HEALTH_CHECK_DATA = True

# External monitoring server configuration
SYNC_SERVER_URL = 'https://monitoring.example.com'
SYNC_APP_ID = 'myapp-production'

# Check every 5 minutes (300 seconds) in production
HEALTH_CHECK_INTERVAL = 300

# ============================================================================
# Additional Production Considerations
# ============================================================================

# Ensure the monitoring server endpoint is accessible
# The health check data will be posted to:
# https://monitoring.example.com/v1/metrics

# Consider setting up firewall rules to allow outbound connections
# to the monitoring server

# For high-availability setups, ensure only one instance runs the monitor
# command to avoid duplicate health check submissions
