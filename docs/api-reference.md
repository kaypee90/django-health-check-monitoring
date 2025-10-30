# API Reference

## Models

### HeathCheckJob

Stores health check execution results in the database.

**Module:** `django_health_check_job.models`

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `name` | CharField(max_length=50) | Name of the health check plugin |
| `status` | IntegerField | Status code (1 = success, 0 = failure) |
| `message` | TextField | Human-readable status message |
| `created_at` | DateTimeField | Timestamp when the record was created (auto_now_add) |
| `updated_at` | DateTimeField | Timestamp when the record was last updated (auto_now) |

**Methods:**

- `__str__()`: Returns the string representation (ID) of the object

**Example Usage:**

```python
from django_health_check_job.models import HeathCheckJob

# Query all health checks
all_checks = HeathCheckJob.objects.all()

# Get failed health checks
failed_checks = HeathCheckJob.objects.filter(status=0)

# Get health checks for a specific plugin
db_checks = HeathCheckJob.objects.filter(name='DatabaseBackend')

# Get recent health checks
from datetime import timedelta
from django.utils import timezone

recent = HeathCheckJob.objects.filter(
    created_at__gte=timezone.now() - timedelta(hours=1)
)
```

## Management Commands

### monitor

Runs health checks continuously at a specified interval.

**Usage:**

```bash
python manage.py monitor
```

**Behavior:**

1. Initializes the health check system
2. Retrieves all registered health check plugins
3. Executes health checks based on `HEALTH_CHECK_INTERVAL` setting
4. Processes results according to configuration:
   - If `PERSIST_HEALTH_CHECK_DATA = True`: Saves to database
   - If `SYNC_HEALTH_CHECK_DATA = True`: Syncs to monitoring server
5. Displays results in console
6. Repeats indefinitely

**Exit Codes:**

- `0`: All health checks passed (only when command is interrupted)
- `1`: One or more health checks failed or error occurred

**Console Output Format:**

```
<plugin_name>        ... <status>
```

Where `<status>` is displayed in:
- Green for successful checks
- Red for failed checks

## Utility Functions

### process_payload(payload)

Processes health check results according to configuration.

**Module:** `django_health_check_job.utils`

**Parameters:**

- `payload` (dict): Health check data containing:
  - `uuid` (str): Unique identifier for the check run
  - `timestamp` (str): ISO 8601 formatted timestamp
  - `checks` (list): List of health check results

**Returns:** None

**Side Effects:**

- Saves data to database if `PERSIST_HEALTH_CHECK_DATA = True`
- Syncs data to monitoring server if `SYNC_HEALTH_CHECK_DATA = True`

**Example:**

```python
from django_health_check_job.utils import process_payload
from datetime import datetime
import uuid

payload = {
    'uuid': str(uuid.uuid4()),
    'timestamp': datetime.utcnow().isoformat(),
    'checks': [
        {
            'name': 'DatabaseBackend',
            'status': 1,
            'message': 'working'
        }
    ]
}

process_payload(payload)
```

### save_health_check_data_to_db(payload)

Saves health check data to the database.

**Module:** `django_health_check_job.utils`

**Parameters:**

- `payload` (dict): Health check data (same format as `process_payload`)

**Returns:** None

**Side Effects:**

- Creates `HeathCheckJob` records in the database using bulk_create

**Example:**

```python
from django_health_check_job.utils import save_health_check_data_to_db

payload = {
    'checks': [
        {'name': 'DatabaseBackend', 'status': 1, 'message': 'working'},
        {'name': 'CacheBackend', 'status': 0, 'message': 'unavailable'},
    ]
}

save_health_check_data_to_db(payload)
```

### sync_health_check_data_to_monitoring_server(payload)

Sends health check data to an external monitoring server.

**Module:** `django_health_check_job.utils`

**Parameters:**

- `payload` (dict): Health check data (same format as `process_payload`)

**Returns:** None

**Raises:**

- `DjangoHealthCheckJobError`: If required settings are missing
- `requests.exceptions.HTTPError`: If the HTTP request fails

**Side Effects:**

- Adds `sync_app_id` to the payload
- Makes POST request to `{SYNC_SERVER_URL}/v1/metrics`

**Required Settings:**

- `SYNC_SERVER_URL`: Base URL of the monitoring server
- `SYNC_APP_ID`: Application identifier

**Example:**

```python
from django_health_check_job.utils import sync_health_check_data_to_monitoring_server

# Requires SYNC_SERVER_URL and SYNC_APP_ID in settings
payload = {
    'uuid': '550e8400-e29b-41d4-a716-446655440000',
    'timestamp': '2023-11-20T12:00:00.000000',
    'checks': [
        {'name': 'DatabaseBackend', 'status': 1, 'message': 'working'}
    ]
}

try:
    sync_health_check_data_to_monitoring_server(payload)
except DjangoHealthCheckJobError as e:
    print(f"Configuration error: {e}")
```

## Exceptions

### DjangoHealthCheckJobError

Custom exception for Django Health Check Monitoring errors.

**Module:** `django_health_check_job.utils`

**Inheritance:** `Exception`

**Usage:**

```python
from django_health_check_job.utils import DjangoHealthCheckJobError

raise DjangoHealthCheckJobError("SYNC_SERVER_URL setting is not set")
```

## Admin Interface

### HeathCheckJobAdmin

Admin interface for viewing and managing health check records.

**Module:** `django_health_check_job.admin`

**Features:**

- **List Display:** Shows id, name, status, message, created_at, updated_at
- **List Filters:** Filter by status, message, name
- **Search Fields:** Search by name and message
- **History List Display:** Shows status in change history

**Accessing:**

Navigate to `/admin/django_health_check_job/heathcheckjob/` in your Django admin.

## Settings Reference

Complete list of available settings:

| Setting | Type | Default | Required | Description |
|---------|------|---------|----------|-------------|
| `HEALTH_CHECK_INTERVAL` | int | 5 | No | Health check interval in seconds |
| `PERSIST_HEALTH_CHECK_DATA` | bool | False | No | Whether to save data to database |
| `SYNC_HEALTH_CHECK_DATA` | bool | False | No | Whether to sync data to monitoring server |
| `SYNC_SERVER_URL` | str | None | Conditional* | Base URL of monitoring server |
| `SYNC_APP_ID` | str | None | Conditional* | Application identifier |

\* Required when `SYNC_HEALTH_CHECK_DATA = True`

## Health Check Payload Schema

The payload format sent to monitoring servers and saved to the database:

```json
{
  "uuid": "string (UUID)",
  "timestamp": "string (ISO 8601)",
  "sync_app_id": "string (added when syncing)",
  "checks": [
    {
      "name": "string",
      "status": "integer (0 or 1)",
      "message": "string"
    }
  ]
}
```

**Field Descriptions:**

- `uuid`: Unique identifier for this health check run (auto-generated)
- `timestamp`: When the health check was performed (auto-generated)
- `sync_app_id`: Application identifier (from `SYNC_APP_ID` setting, added during sync)
- `checks`: Array of individual health check plugin results
  - `name`: Health check plugin identifier (e.g., "DatabaseBackend")
  - `status`: 1 for success, 0 for failure
  - `message`: Human-readable status description

## Integration Points

### Django Health Check

Django Health Check Monitoring integrates with [django-health-check](https://github.com/revsys/django-health-check) plugins.

**Available Plugins:**

- `health_check.db` - Database connectivity
- `health_check.cache` - Cache backend
- `health_check.storage` - Storage backend
- `health_check.contrib.migrations` - Migrations status
- `health_check.contrib.celery` - Celery workers
- `health_check.contrib.celery_ping` - Celery ping
- `health_check.contrib.psutil` - System resources
- `health_check.contrib.rabbitmq` - RabbitMQ
- `health_check.contrib.redis` - Redis
- `health_check.contrib.s3boto3_storage` - S3 storage

### Custom Health Checks

To create custom health checks, follow the django-health-check documentation:

```python
# myapp/health_checks.py
from health_check.backends import BaseHealthCheckBackend

class MyServiceHealthCheck(BaseHealthCheckBackend):
    critical_service = True
    
    def check_status(self):
        # Implement your health check logic
        try:
            # Check your service
            result = my_service.ping()
            if not result:
                self.add_error("Service is not responding")
        except Exception as e:
            self.add_error(f"Service error: {e}")
    
    def identifier(self):
        return "MyService"
```

Register in `myapp/apps.py`:

```python
from django.apps import AppConfig
from health_check.plugins import plugin_dir

class MyAppConfig(AppConfig):
    name = 'myapp'
    
    def ready(self):
        from .health_checks import MyServiceHealthCheck
        plugin_dir.register(MyServiceHealthCheck)
```
