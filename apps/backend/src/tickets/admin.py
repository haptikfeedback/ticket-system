from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "tenant", "assigned_to", "appointment_start", "at_risk", "created_at")
    list_filter = ("status", "tenant")
    search_fields = ("title", "description")
    autocomplete_fields = ("assigned_to",)
