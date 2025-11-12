# Installation Guide

## Requirements

- Python >= 3.7
- Django >= 2.2
- django-health-check >= 3.17.0
- schedule >= 1.2.1

## Installation

### Via pip (recommended)

```bash
pip install django-health-check-job
```

### From source

```bash
git clone https://github.com/kaypee90/django-health-check-monitoring.git
cd django-health-check-monitoring
pip install -e .
```

## Django Setup

### 1. Add to INSTALLED_APPS

Add `django_health_check_job` to your Django project's `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_health_check_job',
    'health_check',                 # Required
    'health_check.db',              # Optional: Database health check
    'health_check.cache',           # Optional: Cache health check
    'health_check.storage',         # Optional: Storage health check
    'health_check.contrib.migrations',  # Optional: Migrations health check
]
```

### 2. Run Migrations

```bash
python manage.py migrate django_health_check_job
```

This will create the necessary database tables to store health check data.

## Verification

To verify the installation, you can run:

```bash
python manage.py check
```

This should complete without errors related to `django_health_check_job`.

## Next Steps

- See [Configuration](configuration.md) for setting up health check monitoring
- See [Usage](usage.md) for examples and common use cases
