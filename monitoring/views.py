from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from monitoring.serializers import HealthCheckJobSerializer


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
