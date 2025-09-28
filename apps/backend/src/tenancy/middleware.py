from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import Tenant
from .current import set_current_tenant

class TenancyMiddleware(MiddlewareMixin):
    # Paths that don't need a tenant (admin/health/static, etc.)
    ALLOWLIST_PREFIXES = ("/admin", "/healthz", "/static", "/media", "/__debug__")

    def process_request(self, request):
        if request.path.startswith(self.ALLOWLIST_PREFIXES):
            return None

        tid = request.headers.get("X-Tenant-ID")
        tslug = request.headers.get("X-Tenant-Slug")

        if not tid and not tslug:
            return JsonResponse(
                {"error": "TENANT_REQUIRED", "detail": "Send X-Tenant-ID or X-Tenant-Slug header."},
                status=400,
            )

        tenant = None
        if tid:
            tenant = Tenant.objects.filter(id=tid, is_active=True).first()
        if tenant is None and tslug:
            tenant = Tenant.objects.filter(slug=tslug.lower(), is_active=True).first()

        if tenant is None:
            return JsonResponse(
                {"error": "TENANT_NOT_FOUND", "detail": "No active tenant matches the provided header."},
                status=400,
            )

        request.tenant = tenant
        set_current_tenant(tenant)
        return None
