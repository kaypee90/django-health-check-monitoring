from django.urls import path
from monitoring.views import HealthCheckJobView

urlpatterns = [
    path("healthcheckjobs/", HealthCheckJobView.as_view(), name="healthcheckjobs"),
]
