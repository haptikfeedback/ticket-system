import os
from django.utils.deprecation import MiddlewareMixin
from .models import Tenant
from .current import set_current_tenant

class TenancyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tenant = None
        tid = request.headers.get("X-Tenant-ID")
        tslug = request.headers.get("X-Tenant-Slug")
        if not (tid or tslug):
            tid = os.getenv("DEFAULT_TENANT_ID")
            tslug = os.getenv("DEFAULT_TENANT_SLUG")
        if tid:
            tenant = Tenant.objects.filter(id=tid, is_active=True).first()
        if tenant is None and tslug:
            tenant = Tenant.objects.filter(slug=tslug, is_active=True).first()
        if tenant is None:
            tenant = Tenant.objects.filter(is_active=True).first()
        request.tenant = tenant
        set_current_tenant(tenant)
