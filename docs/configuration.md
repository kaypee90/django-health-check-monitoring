# Configuration

## Settings

Configure Django Health Check Monitoring by adding the following settings to your Django `settings.py` file.

### HEALTH_CHECK_INTERVAL

**Type:** Integer  
**Default:** `5`  
**Units:** Seconds  
**Required:** No

Defines how often the health check monitor should run.

```python
# Run health checks every 60 seconds
HEALTH_CHECK_INTERVAL = 60
```

### PERSIST_HEALTH_CHECK_DATA

**Type:** Boolean  
**Default:** `False`  
**Required:** No

When set to `True`, health check results will be saved to the database in the `HeathCheckJob` model.

```python
# Enable persistence of health check data
PERSIST_HEALTH_CHECK_DATA = True
```

### SYNC_HEALTH_CHECK_DATA

**Type:** Boolean  
**Default:** `False`  
**Required:** No

When set to `True`, health check results will be synchronized to an external monitoring server.

```python
# Enable syncing to external monitoring server
SYNC_HEALTH_CHECK_DATA = True
```

### SYNC_SERVER_URL

**Type:** String  
**Default:** None  
**Required:** Yes (if `SYNC_HEALTH_CHECK_DATA = True`)

The base URL of your external monitoring server. Health check data will be posted to `{SYNC_SERVER_URL}/v1/metrics`.

```python
SYNC_SERVER_URL = "https://monitoring.example.com"
```

### SYNC_APP_ID

**Type:** String  
**Default:** None  
**Required:** Yes (if `SYNC_HEALTH_CHECK_DATA = True`)

A unique identifier for your application. This ID will be included in the payload sent to the monitoring server.

```python
SYNC_APP_ID = "my-django-app-prod"
```

## Configuration Examples

### Example 1: Local Development (Database Persistence Only)

```python
# settings.py

# Save health check data to local database
PERSIST_HEALTH_CHECK_DATA = True
SYNC_HEALTH_CHECK_DATA = False

# Check every 30 seconds
HEALTH_CHECK_INTERVAL = 30
```

### Example 2: Production (Sync to Monitoring Server)

```python
# settings.py

# Don't persist locally, sync to monitoring server
PERSIST_HEALTH_CHECK_DATA = False
SYNC_HEALTH_CHECK_DATA = True

# Monitoring server configuration
SYNC_SERVER_URL = "https://monitoring.example.com"
SYNC_APP_ID = "my-django-app-prod"

# Check every 5 minutes
HEALTH_CHECK_INTERVAL = 300
```

### Example 3: Both Persistence and Sync

```python
# settings.py

# Save to database AND sync to monitoring server
PERSIST_HEALTH_CHECK_DATA = True
SYNC_HEALTH_CHECK_DATA = True

SYNC_SERVER_URL = "https://monitoring.example.com"
SYNC_APP_ID = "my-django-app-staging"

HEALTH_CHECK_INTERVAL = 60
```

## Health Check Plugins

Django Health Check Monitoring uses django-health-check plugins. Configure which health checks to run by adding the appropriate apps to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_health_check_job',
    'health_check',
    
    # Available health check plugins:
    'health_check.db',                      # Database connectivity check
    'health_check.cache',                   # Cache backend check
    'health_check.storage',                 # Storage backend check
    'health_check.contrib.migrations',      # Migrations check
    'health_check.contrib.celery',          # Celery check (if using Celery)
    'health_check.contrib.celery_ping',     # Celery ping check
    'health_check.contrib.psutil',          # System resources check
    'health_check.contrib.rabbitmq',        # RabbitMQ check
    'health_check.contrib.redis',           # Redis check
    'health_check.contrib.s3boto3_storage', # S3 storage check
]
```

For more information on available plugins and custom health checks, see the [django-health-check documentation](https://github.com/revsys/django-health-check).

## Monitoring Server API

If you enable `SYNC_HEALTH_CHECK_DATA`, the monitoring server should accept POST requests to `/v1/metrics` with the following JSON payload:

```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2023-11-20T12:00:00.000000",
  "sync_app_id": "my-django-app-prod",
  "checks": [
    {
      "name": "DatabaseBackend",
      "status": 1,
      "message": "working"
    },
    {
      "name": "CacheBackend",
      "status": 1,
      "message": "working"
    }
  ]
}
```

**Field Descriptions:**
- `uuid`: Unique identifier for this health check run
- `timestamp`: ISO 8601 formatted timestamp
- `sync_app_id`: Your application identifier (from `SYNC_APP_ID` setting)
- `checks`: Array of health check results
  - `name`: Plugin identifier
  - `status`: Status code (1 = success, 0 = failure)
  - `message`: Human-readable status message
