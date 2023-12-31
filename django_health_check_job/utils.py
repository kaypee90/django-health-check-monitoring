import logging
from django.conf import settings

from django_health_check_job.models import HeathCheckJob

logger = logging.getLogger(__name__)


def process_payload(payload):
    """
    Processes the health check payload
    """
    persist_data = getattr(settings, "PERSIST_HEALTH_CHECK_DATA", False)

    sync_data = getattr(settings, "SYNC_HEALTH_CHECK_DATA", False)

    if persist_data:
        save_health_check_data_to_db(payload)

    if sync_data:
        sync_health_check_data_to_monitoring_server(payload)


def save_health_check_data_to_db(payload):
    """
    Saves the health check data to the database
    """
    logging.debug("saving health check data to database")
    heath_check_models = []
    for item in payload.get("data", []):
        heath_check_models.append(HeathCheckJob(**item))
    HeathCheckJob.objects.bulk_create(heath_check_models)


def sync_health_check_data_to_monitoring_server(payload):
    """
    Syncs the health check data with the monitoring server
    """
    logging.debug("Syncing health check data to monitoring server")
    server_url = getattr(settings, "SYNC_SERVER_URL", False)

    if not server_url:
        raise Exception("SYNC_SERVER_URL setting is not set")

    import requests

    response = requests.post(
        url=server_url + "/healthcheckjobs", data=payload, timeout=5
    )
    response.raise_for_status()
