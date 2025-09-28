from contextvars import ContextVar
_current_tenant = ContextVar("current_tenant", default=None)

def set_current_tenant(tenant):
    _current_tenant.set(tenant)

def get_current_tenant():
    return _current_tenant.get()
