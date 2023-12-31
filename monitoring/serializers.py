from rest_framework import serializers
from monitoring.models import Service, HeathCheck, HeathCheckPlugin


class HeathCheckPluginSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=50)
    status = serializers.IntegerField(required=True)
    message = serializers.CharField(required=True)

    class Meta:
        fields = ("name", "status", "message")


class HealthCheckJobSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True, max_length=256)
    timestamp = serializers.DateTimeField(required=True)
    sync_app_id = serializers.CharField(required=True, max_length=256, write_only=True)
    checks = HeathCheckPluginSerializer(many=True, write_only=True)

    class Meta:
        fields = ("uuid", "timestamp", "sync_app_id", "checks")

    def create(self, validated_data):
        service_identifier = validated_data.pop("sync_app_id")
        try:
            service = Service.objects.get(identifier=service_identifier)
        except Service.DoesNotExist:
            raise serializers.ValidationError("Invalid sync_app_id provided!")

        source = self.context["source"]

        checks = validated_data.pop("checks")
        health_check = HeathCheck.objects.create(
            uuid=validated_data.get("uuid"),
            timestamp=validated_data.get("timestamp"),
            source=source,
            service=service,
        )

        plugins_models = []

        for check in checks:
            plugins_models.append(HeathCheckPlugin(health_check=health_check, **check))

        HeathCheckPlugin.objects.bulk_create(plugins_models)

        return health_check
