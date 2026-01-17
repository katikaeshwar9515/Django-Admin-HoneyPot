from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import LoginAttempt,BlackList, HoneyPotHit

# Register your models here.
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "ip_address",
        "path",
        "created_date",
    ]

admin.site.register(LoginAttempt,LoginAttemptAdmin)
admin.site.register(BlackList)


@admin.register(HoneyPotHit)
class HoneyPotHitAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "path", "created_date", "user_agent"]
    search_fields = ["ip_address", "path", "user_agent"]
    list_filter = ["created_date"]
    actions = ["export_csv"]

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=honeypot_hits.csv"
        writer = csv.writer(response)
        writer.writerow(["ip_address", "path", "user_agent", "created_date", "session_key"])
        for hit in queryset:
            writer.writerow([hit.ip_address, hit.path, hit.user_agent, hit.created_date, hit.session_key])
        return response

    export_csv.short_description = "Export selected to CSV"
