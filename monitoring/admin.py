from django.contrib import admin

from monitoring.models import Service, HeathCheck, HeathCheckPlugin


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "identifier",
        "name",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)


class HeathCheckAdmin(admin.ModelAdmin):
    list_filter = ("source",)

    list_display = ("id", "uuid", "timestamp", "source", "created_at", "updated_at")
    search_fields = (
        "uuid",
        "source",
    )


class HeathCheckPluginAdmin(admin.ModelAdmin):
    list_filter = (
        "name",
        "status",
    )

    list_display = ("id", "name", "status", "message", "created_at", "updated_at")
    search_fields = (
        "name",
        "message",
    )


admin.site.register(Service, ServiceAdmin)
admin.site.register(HeathCheck, HeathCheckAdmin)
admin.site.register(HeathCheckPlugin, HeathCheckPluginAdmin)
