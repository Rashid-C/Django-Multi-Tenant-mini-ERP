from django.http import JsonResponse
from tenants.models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Look for the tenant identifier header
        tenant_id = request.headers.get('X-Tenant-ID')
        
        # Exclude administrative paths if necessary
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        if not tenant_id:
            return JsonResponse({'error': 'X-Tenant-ID header missing.'}, status=400)

        try:
            # 2. Bind the resolved tenant object directly onto the request thread context
            request.tenant = Tenant.objects.get(id=tenant_id, is_active=True)
        except Tenant.DoesNotExist:
            return JsonResponse({'error': 'Invalid or inactive Tenant.'}, status=403)

        return self.get_response(request)