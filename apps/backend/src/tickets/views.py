from rest_framework import viewsets, permissions
from .models import Ticket
from .serializers import TicketSerializer

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ("GET", "HEAD", "OPTIONS") or (request.user and request.user.is_authenticated)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        qs = Ticket.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant, created_by=getattr(self.request, "user", None))
