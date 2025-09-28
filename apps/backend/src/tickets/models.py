import uuid
from django.db import models
from django.contrib.auth import get_user_model
from tenancy.models import Tenant

User = get_user_model()

class Ticket(models.Model):
    class Status(models.TextChoices):
        CREATED   = "created", "Created"
        ROUTED    = "routed", "Routed"
        ASSIGNED  = "assigned", "Assigned"
        CONFIRMED = "confirmed", "Confirmed"
        ENROUTE   = "enroute", "EnRoute"
        ONSITE    = "onsite", "OnSite"
        WORKSTART = "workstart", "Work Start"
        WORKSTOP  = "workstop", "Work Stop"
        COMPLETED = "completed", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="tickets")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets_created")
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets_assigned")

    appointment_start = models.DateTimeField(null=True, blank=True)
    appointment_end = models.DateTimeField(null=True, blank=True)

    confirmed_at = models.DateTimeField(null=True, blank=True)
    enroute_at = models.DateTimeField(null=True, blank=True)
    onsite_at = models.DateTimeField(null=True, blank=True)
    work_start_at = models.DateTimeField(null=True, blank=True)
    work_stop_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def at_risk(self) -> bool:
        from django.utils import timezone
        now = timezone.now()
        if self.appointment_start and self.status in {self.Status.CREATED, self.Status.ROUTED, self.Status.ASSIGNED, self.Status.CONFIRMED}:
            if now >= self.appointment_start and not self.enroute_at:
                if (now - self.appointment_start).total_seconds() >= 30*60:
                    return True
        if self.appointment_start and self.status in {self.Status.ASSIGNED, self.Status.CONFIRMED, self.Status.ENROUTE, self.Status.ONSITE}:
            if now >= self.appointment_start and not self.work_start_at:
                return True
        return False

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"
