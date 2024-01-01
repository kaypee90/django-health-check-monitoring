from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from monitoring.models import Service, HeathCheck, HeathCheckPlugin


class TestHealthCheckView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sync_app_id = "0171d964-1b85-4fb8-9ef3-3fef891d92dc"

        Service.objects.create(name="test_health_check", identifier=self.sync_app_id)

    def test_create_health_check_jobs_should_return_status_ok(self):
        url = "/v1/healthcheckjobs/"
        uuid = "5b943126-60c6-4c8a-9139-9ec161925ed6"

        payload = {
            "uuid": uuid,
            "timestamp": "2023-12-31 13:57:48.120127",
            "sync_app_id": self.sync_app_id,
            "checks": [
                {
                    "name": "MigrationsHealthCheck",
                    "message": "working",
                    "status": 1,
                },
                {
                    "name": "DatabaseHealthCheck",
                    "message": "working",
                    "status": 1,
                },
            ],
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        health_check = HeathCheck.objects.get(uuid=uuid)
        self.assertEqual(str(health_check.service.identifier), self.sync_app_id)
        self.assertIsNotNone(health_check.source)

        jobs = HeathCheckPlugin.objects.filter(health_check_id=health_check.id)
        self.assertEqual(jobs.count(), 2)

        for job in jobs:
            self.assertEqual(job.status, 1)
            self.assertEqual(job.message, "working")

    def test_create_health_check_jobs_with_invalid_payload_should_return_status_bad_request(
        self,
    ):
        url = "/v1/healthcheckjobs/"
        uuid = "5b943126-60c6-4c8a-9139-9ec161925ed6"

        payload = {
            "uuid": uuid,
            "timestamp": "",
            "sync_app_id": "5b943126",
            "checks": [
                {
                    "name": "MigrationsHealthCheck",
                    "message": "",
                    "status": None,
                },
                {
                    "name": None,
                    "message": "working",
                    "status": 1,
                },
            ],
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
