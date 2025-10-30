# Quick Start Guide

Get Django Health Check Monitoring up and running in 5 minutes!

## 1. Install

```bash
pip install django-health-check-job
```

## 2. Configure Django

Add to your `settings.py`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'django_health_check_job',
    'health_check',
    'health_check.db',
    'health_check.cache',
]

# Basic configuration
PERSIST_HEALTH_CHECK_DATA = True  # Save to database
HEALTH_CHECK_INTERVAL = 60        # Check every 60 seconds
```

## 3. Run Migrations

```bash
python manage.py migrate
```

## 4. Start Monitoring

```bash
python manage.py monitor
```

You should see output like:

```
DatabaseBackend          ... working 
CacheBackend            ... working 
```

## 5. View Results

Visit your Django admin at `/admin/django_health_check_job/heathcheckjob/` to see historical health check data!

## What's Next?

### Production Setup

For production, sync to a monitoring server instead of persisting locally:

```python
PERSIST_HEALTH_CHECK_DATA = False
SYNC_HEALTH_CHECK_DATA = True
SYNC_SERVER_URL = "https://monitoring.example.com"
SYNC_APP_ID = "my-app-production"
HEALTH_CHECK_INTERVAL = 300  # 5 minutes
```

### Run as a Service

Deploy the monitor as a background service:

- **Docker**: See [examples/docker-compose.yml](../examples/docker-compose.yml)
- **Systemd**: See [examples/systemd-service.service](../examples/systemd-service.service)
- **Supervisor**: See [examples/supervisor.conf](../examples/supervisor.conf)

### Add More Health Checks

Enable additional health check plugins:

```python
INSTALLED_APPS += [
    'health_check.contrib.redis',    # Redis health check
    'health_check.contrib.celery',   # Celery health check
    'health_check.contrib.psutil',   # System resources check
]
```

### Troubleshooting

**Monitor won't start?**
- Verify all apps are in `INSTALLED_APPS`
- Run `python manage.py migrate`
- Check for errors: `python manage.py check`

**No health checks running?**
- Ensure health_check plugins are installed
- Check that `HEALTH_CHECK_INTERVAL` is set
- Look for error messages in console output

## Learn More

- 📚 [Full Documentation](README.md)
- ⚙️ [Configuration Options](configuration.md)
- 🎯 [Usage Guide](usage.md)
- 📖 [API Reference](api-reference.md)
- 💡 [Examples](../examples/)

## Common Patterns

### Development (Local Testing)

```python
PERSIST_HEALTH_CHECK_DATA = True
SYNC_HEALTH_CHECK_DATA = False
HEALTH_CHECK_INTERVAL = 30
```

### Staging (Testing External Sync)

```python
PERSIST_HEALTH_CHECK_DATA = True
SYNC_HEALTH_CHECK_DATA = True
SYNC_SERVER_URL = "https://staging-monitoring.example.com"
SYNC_APP_ID = "my-app-staging"
HEALTH_CHECK_INTERVAL = 60
```

### Production (External Monitoring Only)

```python
PERSIST_HEALTH_CHECK_DATA = False
SYNC_HEALTH_CHECK_DATA = True
SYNC_SERVER_URL = "https://monitoring.example.com"
SYNC_APP_ID = "my-app-production"
HEALTH_CHECK_INTERVAL = 300
```

## That's It!

You now have health check monitoring running on your Django application. The monitor will continuously check your application's health and store/sync the results as configured.

For more detailed information, see the [complete documentation](README.md).
