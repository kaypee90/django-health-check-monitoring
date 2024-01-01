from django.db import models


class Core(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class HeathCheckJob(Core):
    name = models.CharField(max_length=50)
    status = models.IntegerField()
    message = models.TextField()
