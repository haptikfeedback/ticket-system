from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tickets.views import TicketViewSet

def health(_):
    return HttpResponse("OK", content_type="text/plain")

def home(_):
    return HttpResponse("<h1>Ticket System</h1><p>Django is running in Docker.</p>")

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("healthz", health),
    path("api/", include(router.urls)),
]
