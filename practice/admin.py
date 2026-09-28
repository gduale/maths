from django.contrib import admin

from .models import UsageCounter


@admin.register(UsageCounter)
class UsageCounterAdmin(admin.ModelAdmin):
    list_display = ("__str__", "answered_questions", "completed_series")
    readonly_fields = ("answered_questions", "completed_series")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
