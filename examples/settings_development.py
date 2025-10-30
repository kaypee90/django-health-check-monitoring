"""
Example Django settings for development environment with Django Health Check Monitoring.

This configuration enables local database persistence for debugging and development.
"""

# Basic Django settings (you'll have more of these in your actual settings.py)
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
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
    'health_check.db',              # Database health check
    'health_check.cache',           # Cache health check
    'health_check.storage',         # Storage health check
    'health_check.contrib.migrations',  # Migrations health check
]

# Cache configuration for health checks
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# ============================================================================
# Django Health Check Monitoring Configuration
# ============================================================================

# Enable database persistence for development/debugging
PERSIST_HEALTH_CHECK_DATA = True

# Disable external sync in development
SYNC_HEALTH_CHECK_DATA = False

# Check every 30 seconds (more frequent for local testing)
HEALTH_CHECK_INTERVAL = 30

# Note: SYNC_SERVER_URL and SYNC_APP_ID are not needed when SYNC_HEALTH_CHECK_DATA is False
