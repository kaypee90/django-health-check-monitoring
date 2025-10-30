# Usage Guide

## Quick Start

After installing and configuring Django Health Check Monitoring, you can start monitoring your application's health.

### Running the Monitor Command

The main way to use Django Health Check Monitoring is through the `monitor` management command:

```bash
python manage.py monitor
```

This command will:
1. Start a continuous monitoring loop
2. Run all configured health checks at the interval specified by `HEALTH_CHECK_INTERVAL`
3. Process the results according to your configuration (persist to database and/or sync to monitoring server)
4. Display health check results in the console

### Example Output

```
DatabaseBackend          ... working 
CacheBackend            ... working 
StorageHealthCheck      ... working 
```

## Running as a Background Service

### Using systemd (Linux)

Create a systemd service file `/etc/systemd/system/django-health-monitor.service`:

```ini
[Unit]
Description=Django Health Check Monitor
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/django/project
Environment="DJANGO_SETTINGS_MODULE=config.settings.production"
ExecStart=/path/to/venv/bin/python manage.py monitor
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable django-health-monitor
sudo systemctl start django-health-monitor
sudo systemctl status django-health-monitor
```

### Using Supervisor

Create a supervisor configuration file `/etc/supervisor/conf.d/django-health-monitor.conf`:

```ini
[program:django-health-monitor]
command=/path/to/venv/bin/python manage.py monitor
directory=/path/to/your/django/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/django-health-monitor.log
environment=DJANGO_SETTINGS_MODULE="config.settings.production"
```

Then reload supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start django-health-monitor
```

### Using Docker

Add a service to your `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    # ... your web service configuration
    
  health-monitor:
    build: .
    command: python manage.py monitor
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
    depends_on:
      - web
      - db
      - redis
    restart: unless-stopped
```

## Viewing Health Check Data

### Admin Interface

If you have `PERSIST_HEALTH_CHECK_DATA = True`, you can view historical health check data in the Django Admin:

1. Navigate to `/admin/`
2. Log in with your superuser credentials
3. Click on "Heath check jobs"
4. View, filter, and search health check records

The admin interface provides:
- **Filtering** by status, message, and name
- **Search** by name and message
- **Sorting** by any field
- **Date-based filtering** by created_at and updated_at

### Querying from Code

You can query health check data programmatically:

```python
from django_health_check_job.models import HeathCheckJob
from datetime import timedelta
from django.utils import timezone

# Get all health checks from the last hour
recent_checks = HeathCheckJob.objects.filter(
    created_at__gte=timezone.now() - timedelta(hours=1)
)

# Get failed health checks
failed_checks = HeathCheckJob.objects.filter(status=0)

# Get health checks for a specific plugin
db_checks = HeathCheckJob.objects.filter(name='DatabaseBackend')

# Get the most recent health check for each plugin
from django.db.models import Max

latest_checks = HeathCheckJob.objects.values('name').annotate(
    latest=Max('created_at')
)
```

## Integrating with Monitoring Systems

### Example: Custom Monitoring Dashboard

If you're syncing data to a monitoring server, you can build a custom dashboard that receives the health check data:

```python
# monitoring_server/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def receive_metrics(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Process the health check data
        app_id = data.get('sync_app_id')
        timestamp = data.get('timestamp')
        checks = data.get('checks', [])
        
        # Store in your monitoring database
        # Send alerts if any checks failed
        # Update dashboard metrics
        
        failed_checks = [c for c in checks if c['status'] == 0]
        if failed_checks:
            # Send alert
            send_alert(app_id, failed_checks)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
```

### Example: Prometheus Integration

You could create a Prometheus exporter endpoint:

```python
# myapp/views.py
from django.http import HttpResponse
from django_health_check_job.models import HeathCheckJob
from django.db.models import Max

def health_metrics(request):
    """Prometheus metrics endpoint"""
    metrics = []
    
    # Get latest health check for each plugin
    latest_by_plugin = HeathCheckJob.objects.values('name').annotate(
        latest_time=Max('created_at')
    )
    
    for item in latest_by_plugin:
        check = HeathCheckJob.objects.get(
            name=item['name'],
            created_at=item['latest_time']
        )
        
        # Create Prometheus metrics
        metrics.append(
            f'django_health_check{{plugin="{check.name}"}} {check.status}'
        )
    
    return HttpResponse('\n'.join(metrics), content_type='text/plain')
```

## Best Practices

### 1. Choose Appropriate Check Intervals

- **Development**: 30-60 seconds for quick feedback
- **Staging**: 60-300 seconds for regular monitoring
- **Production**: 300-600 seconds to reduce overhead

### 2. Monitor Resource Usage

The monitor command runs continuously. Monitor its resource usage:

```bash
# Check process memory and CPU
ps aux | grep "manage.py monitor"

# Monitor with htop
htop -p $(pgrep -f "manage.py monitor")
```

### 3. Log Rotation

Ensure logs are rotated to prevent disk space issues:

```bash
# /etc/logrotate.d/django-health-monitor
/var/log/django-health-monitor.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

### 4. Alerting

Set up alerts for health check failures:

- **Email alerts** for critical failures
- **Slack/Teams notifications** for team awareness
- **PagerDuty integration** for on-call support

### 5. Data Retention

If using database persistence, implement a cleanup strategy:

```python
# Create a management command: cleanup_health_checks.py
from django.core.management.base import BaseCommand
from django_health_check_job.models import HeathCheckJob
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Delete health checks older than 30 days
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted = HeathCheckJob.objects.filter(
            created_at__lt=cutoff_date
        ).delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Deleted {deleted[0]} old health check records')
        )
```

Run this as a periodic task (cron or Celery beat):

```bash
# Crontab: Run cleanup daily at 2 AM
0 2 * * * cd /path/to/project && /path/to/venv/bin/python manage.py cleanup_health_checks
```

## Troubleshooting

### Monitor Command Won't Start

**Problem**: Command exits immediately or with error

**Solutions**:
- Check that all required apps are in `INSTALLED_APPS`
- Verify database migrations are applied: `python manage.py migrate`
- Check for configuration errors in settings
- Look for dependency issues: `pip list | grep health-check`

### Health Checks Always Failing

**Problem**: All health checks report failures

**Solutions**:
- Test each health check plugin individually
- Check database connectivity
- Verify cache backend is running
- Check storage backend permissions
- Review application logs for errors

### High Memory Usage

**Problem**: Monitor process consuming too much memory

**Solutions**:
- Reduce `HEALTH_CHECK_INTERVAL` if checking too frequently
- Disable `PERSIST_HEALTH_CHECK_DATA` if not needed
- Implement data cleanup for old records
- Consider using external monitoring instead

### Sync to Monitoring Server Failing

**Problem**: Data not reaching monitoring server

**Solutions**:
- Verify `SYNC_SERVER_URL` is correct and accessible
- Check network connectivity to monitoring server
- Verify monitoring server is accepting POST requests
- Check for firewall or security group rules blocking traffic
- Review application logs for HTTP errors
- Increase timeout if needed (modify `utils.py`)
