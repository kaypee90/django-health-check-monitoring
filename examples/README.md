# Examples

This directory contains example configurations for Django Health Check Monitoring in various environments and setups.

## Configuration Examples

### Development Settings

**File:** `settings_development.py`

Example Django settings for local development:
- Enables database persistence for debugging
- Disables external sync
- Short check interval (30 seconds) for quick feedback

### Production Settings

**File:** `settings_production.py`

Example Django settings for production:
- Disables database persistence to reduce DB load
- Enables external monitoring server sync
- Longer check interval (5 minutes)
- Includes additional production health check plugins

## Deployment Examples

### Docker Compose

**File:** `docker-compose.yml`

Complete Docker Compose setup including:
- Web service running the Django application
- Separate health-monitor service running the monitor command
- PostgreSQL database
- Redis cache
- Volume management

**Usage:**

```bash
docker-compose up -d
```

**Monitoring:**

```bash
# View health monitor logs
docker-compose logs -f health-monitor

# Check service status
docker-compose ps
```

### Systemd Service

**File:** `systemd-service.service`

Systemd service configuration for running the monitor as a system service.

**Installation:**

```bash
# Copy to systemd directory
sudo cp systemd-service.service /etc/systemd/system/django-health-monitor.service

# Edit to match your environment
sudo nano /etc/systemd/system/django-health-monitor.service

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable django-health-monitor

# Start service
sudo systemctl start django-health-monitor

# Check status
sudo systemctl status django-health-monitor
```

**Viewing Logs:**

```bash
# Follow logs
sudo journalctl -u django-health-monitor -f

# View recent logs
sudo journalctl -u django-health-monitor -n 100
```

### Supervisor

**File:** `supervisor.conf`

Supervisor configuration for process management.

**Installation:**

```bash
# Copy to supervisor conf.d directory
sudo cp supervisor.conf /etc/supervisor/conf.d/django-health-monitor.conf

# Edit to match your environment
sudo nano /etc/supervisor/conf.d/django-health-monitor.conf

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Start the monitor
sudo supervisorctl start django-health-monitor

# Check status
sudo supervisorctl status django-health-monitor
```

**Viewing Logs:**

```bash
# Follow logs
sudo tail -f /var/log/supervisor/django-health-monitor.log
```

## Customization

All examples use environment variables that you can customize:

- `DJANGO_SETTINGS_MODULE` - Your Django settings module
- `PERSIST_HEALTH_CHECK_DATA` - Whether to save to database (true/false)
- `SYNC_HEALTH_CHECK_DATA` - Whether to sync to monitoring server (true/false)
- `SYNC_SERVER_URL` - URL of your monitoring server
- `SYNC_APP_ID` - Unique identifier for your application
- `HEALTH_CHECK_INTERVAL` - Check interval in seconds

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Deploy with Health Monitoring

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy application
        run: |
          # Your deployment steps
          
      - name: Start health monitor
        run: |
          ssh user@server "sudo systemctl restart django-health-monitor"
```

### GitLab CI Example

```yaml
deploy:
  stage: deploy
  script:
    - # Your deployment steps
    - ssh user@server "sudo systemctl restart django-health-monitor"
  only:
    - main
```

## Environment-Specific Notes

### Development

- Use database persistence to review historical data
- Short check intervals for quick feedback
- Consider using Django's development server and a separate terminal for the monitor

### Staging

- Balance between development and production settings
- May want both persistence and sync
- Moderate check interval (1-2 minutes)

### Production

- Minimize database operations (disable persistence)
- Always sync to external monitoring
- Longer check intervals to reduce overhead (5-10 minutes)
- Ensure proper monitoring and alerting is set up
- Consider high-availability scenarios (only run one monitor instance)

## High Availability Considerations

When running multiple application instances:

1. **Single Monitor Instance**: Only run the monitor command on one instance to avoid duplicate submissions

2. **Leader Election**: Use a distributed lock (Redis, Zookeeper) to elect a leader:

```python
# Custom monitor wrapper with leader election
import redis
from django.core.management import call_command

def run_monitor_with_leader_election():
    r = redis.Redis(host='redis', port=6379)
    lock = r.lock('health-monitor-leader', timeout=60)
    
    if lock.acquire(blocking=False):
        try:
            call_command('monitor')
        finally:
            lock.release()
```

3. **Separate Monitor Service**: Deploy the monitor as a separate service/container that only runs once

## Troubleshooting

### Monitor Won't Start

- Check that all paths are correct
- Verify Python virtual environment activation
- Ensure all dependencies are installed
- Check environment variable syntax
- Review service logs

### High Resource Usage

- Increase `HEALTH_CHECK_INTERVAL`
- Disable `PERSIST_HEALTH_CHECK_DATA`
- Review which health check plugins are enabled

### Monitoring Server Connection Issues

- Verify `SYNC_SERVER_URL` is accessible
- Check firewall rules
- Review network connectivity
- Check monitoring server logs

## Additional Resources

- [Installation Guide](../docs/installation.md)
- [Configuration Documentation](../docs/configuration.md)
- [Usage Guide](../docs/usage.md)
- [API Reference](../docs/api-reference.md)
