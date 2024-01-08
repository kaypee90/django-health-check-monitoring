from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from rest_framework.decorators import api_view

from monitoring.serializers import HealthCheckJobSerializer
from monitoring.models import HeathCheckPlugin
from django.db.models import Count
from datetime import datetime


@api_view(
    [
        "GET",
    ]
)
def health_check(_):
    """
    Health check endpoint, always returns 200 status code
    """
    return HttpResponse(status=200)


class HealthCheckJobView(APIView):
    serializer_class = HealthCheckJobSerializer

    def post(self, request, *args, **kwargs):
        """
        Creates health check jobs
        """
        serializer = self.serializer_class(
            data=request.data, context={"source": request.build_absolute_uri()}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        Gets health Check Data
        """
        start_date_str = request.GET.get("start_date")
        end_date_str = request.GET.get("end_date")

        queryset = HeathCheckPlugin.objects.all()

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                queryset = queryset.filter(
                    created_at__gte=start_date, created_at__lte=end_date
                )
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        result = queryset.values("name", "status").annotate(count=Count("id"))

        return Response({"data": result}, status=status.HTTP_200_OK)
