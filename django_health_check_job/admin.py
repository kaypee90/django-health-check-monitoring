from django.contrib import admin

from django_health_check_job.models import HeathCheckJob


class HeathCheckJobAdmin(admin.ModelAdmin):
    list_filter = (
        "status",
        "message",
    )
    history_list_display = ["status"]
    list_display = ("id", "name", "status", "message", "created_at", "updated_at")
    search_fields = (
        "name",
        "message",
    )


admin.site.register(HeathCheckJob, HeathCheckJobAdmin)
