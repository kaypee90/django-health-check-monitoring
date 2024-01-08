from django.urls import path
from monitoring.views import HealthCheckJobView, health_check

urlpatterns = [
    path("_ping/", health_check),
    path("healthcheckjobs/", HealthCheckJobView.as_view(), name="healthcheckjobs"),
]
