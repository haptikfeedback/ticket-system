from django.http import JsonResponse
from .tasks import ping

def enqueue_ping(request):
    r = ping.delay("from-http")
    return JsonResponse({"task_id": r.id})
