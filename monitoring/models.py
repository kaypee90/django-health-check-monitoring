import uuid
from django.db import models


class Core(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Service(Core):
    identifier = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "identifier",
                ]
            ),
        ]

    def __str__(self):
        return str(self.identifier)


class HeathCheck(Core):
    uuid = models.CharField(max_length=256)
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=256)
    service = models.ForeignKey("Service", on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "timestamp",
                ]
            ),
        ]

    def __str__(self):
        return self.uuid


class HeathCheckPlugin(Core):
    name = models.CharField(max_length=50)
    status = models.IntegerField()
    message = models.TextField()
    health_check = models.ForeignKey("HeathCheck", on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
        ]

    def __str__(self):
        return self.name + " " + str(self.id)
