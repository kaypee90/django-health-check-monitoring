# Django Health Check Monitoring Documentation

Welcome to the Django Health Check Monitoring documentation!

## Table of Contents

### Getting Started

1. **[Quick Start Guide](quickstart.md)** ⚡ - Get up and running in 5 minutes!

2. **[Installation Guide](installation.md)** - Install and set up Django Health Check Monitoring
   - Requirements
   - Installation methods (pip, from source)
   - Django setup and configuration
   - Running migrations

3. **[Configuration](configuration.md)** - Configure health check monitoring
   - All available settings explained
   - Configuration examples for different environments
   - Health check plugin configuration
   - Monitoring server API specification

4. **[Usage Guide](usage.md)** - Learn how to use Django Health Check Monitoring
   - Running the monitor command
   - Running as a background service (systemd, supervisor, Docker)
   - Viewing health check data
   - Integration with monitoring systems
   - Best practices
   - Troubleshooting

### Reference

5. **[API Reference](api-reference.md)** - Complete API documentation
   - Models (HeathCheckJob)
   - Management commands (monitor)
   - Utility functions
   - Exceptions
   - Admin interface
   - Settings reference
   - Payload schema
   - Integration points

## Quick Links

- [GitHub Repository](https://github.com/kaypee90/django-health-check-monitoring)
- [Issue Tracker](https://github.com/kaypee90/django-health-check-monitoring/issues)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [License](../LICENSE)

## Overview

Django Health Check Monitoring is a Python library that enhances monitoring capabilities in Django applications by:

- Capturing health check data from django-health-check plugins
- Storing health check results in your database
- Syncing health check data to external monitoring services
- Providing a scheduled monitoring system
- Offering an admin interface for viewing historical data

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Django Application                   │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌─────────────────────────────────────────────┐   │
│  │    django-health-check Plugins               │   │
│  │  • DatabaseBackend                           │   │
│  │  • CacheBackend                              │   │
│  │  • StorageHealthCheck                        │   │
│  │  • Custom Plugins                            │   │
│  └──────────────┬──────────────────────────────┘   │
│                 │                                    │
│                 ▼                                    │
│  ┌─────────────────────────────────────────────┐   │
│  │  Django Health Check Monitoring              │   │
│  │  (monitor command)                           │   │
│  │  • Runs health checks on schedule            │   │
│  │  • Collects results                          │   │
│  │  • Processes payload                         │   │
│  └─────┬──────────────────────┬────────────────┘   │
│        │                      │                     │
│        │                      │                     │
└────────┼──────────────────────┼─────────────────────┘
         │                      │
         ▼                      ▼
  ┌──────────────┐     ┌──────────────────┐
  │   Database   │     │ Monitoring Server│
  │  (Optional)  │     │    (Optional)    │
  └──────────────┘     └──────────────────┘
```

## Features at a Glance

### Database Persistence

Store health check results in your Django database for:
- Historical analysis
- Trend identification
- Compliance and auditing
- Debugging past issues

### External Monitoring Integration

Sync health check data to external monitoring services:
- Real-time dashboards
- Alerting systems
- Centralized monitoring for multiple applications
- Custom visualization

### Flexible Configuration

- Configurable check intervals
- Optional database persistence
- Optional external sync
- Support for all django-health-check plugins

### Admin Interface

View and manage health check data through Django admin:
- Filter by status, name, message
- Search functionality
- Date-based filtering
- Detailed record inspection

## Common Use Cases

### 1. Local Development

Monitor application health during development:

```python
PERSIST_HEALTH_CHECK_DATA = True
SYNC_HEALTH_CHECK_DATA = False
HEALTH_CHECK_INTERVAL = 30
```

### 2. Production Monitoring

Send health data to monitoring service:

```python
PERSIST_HEALTH_CHECK_DATA = False
SYNC_HEALTH_CHECK_DATA = True
SYNC_SERVER_URL = "https://monitoring.example.com"
SYNC_APP_ID = "production-app"
HEALTH_CHECK_INTERVAL = 300
```

### 3. Compliance and Auditing

Store all health check data for compliance:

```python
PERSIST_HEALTH_CHECK_DATA = True
SYNC_HEALTH_CHECK_DATA = True
SYNC_SERVER_URL = "https://monitoring.example.com"
SYNC_APP_ID = "production-app"
HEALTH_CHECK_INTERVAL = 60
```

## Support

- **Documentation Issues**: If you find errors or unclear sections in the documentation, please [open an issue](https://github.com/kaypee90/django-health-check-monitoring/issues)
- **Questions**: For questions about usage, check the [Usage Guide](usage.md) or open a discussion
- **Bug Reports**: Report bugs in the [issue tracker](https://github.com/kaypee90/django-health-check-monitoring/issues)
- **Feature Requests**: Suggest new features by opening an issue with the "enhancement" label

## Contributing to Documentation

Documentation contributions are welcome! See our [Contributing Guidelines](../CONTRIBUTING.md) for details on how to:

- Fix typos or errors
- Improve explanations
- Add examples
- Translate documentation

## Version History

- **v0.1.0** - Initial release
  - Basic health check monitoring
  - Database persistence
  - External sync support
  - Admin interface

---

*Last updated: 2023*
