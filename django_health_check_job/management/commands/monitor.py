import sys
import time
from datetime import datetime
import uuid

from django.core.management.base import BaseCommand
from django.http import Http404
from django.conf import settings

from health_check.mixins import CheckMixin
import schedule

from django_health_check_job.utils import process_payload


class HealthCheck(CheckMixin):
    def get_plugins(self):
        plugins = super().plugins

        return {v.identifier(): v for v in plugins}


class Command(BaseCommand, HealthCheck):
    help = "Run health checks and exit 0 if everything went well."

    def job(self):
        try:
            errors = self.check()
        except Http404 as e:
            self.stdout.write(str(e))
            sys.exit(1)

        plugin_data = []

        for plugin_identifier, plugin in self.get_plugins().items():
            style_func = self.style.SUCCESS if not plugin.errors else self.style.ERROR
            self.stdout.write(
                "{:<24} ... {} \n".format(
                    plugin_identifier, style_func(plugin.pretty_status())
                )
            )

            plugin_data.append(
                {
                    "name": plugin_identifier,
                    "message": plugin.pretty_status(),
                    "status": plugin.status,
                }
            )

        payload = {
            "uuid": str(uuid.uuid4()),
            "timestamp": datetime.utcnow(),
            "checks": plugin_data,
        }

        process_payload(payload)

        if errors:
            sys.exit(1)

    def handle(self, *args, **options):
        health_check_interval = getattr(
            settings, "HEALTH_CHECK_INTERVAL", 5
        )  # in seconds
        schedule.every(int(health_check_interval)).seconds.do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(1)
