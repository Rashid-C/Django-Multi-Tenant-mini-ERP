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
    
    
    
class TenantSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # If the user is authenticated via JWT
        if request.user.is_authenticated:
            # Lock the request context strictly to the user's assigned tenant
            request.tenant = request.user.profile.tenant
        else:
            # Fallback for open registration/login endpoints using the header
            tenant_id = request.headers.get('X-Tenant-ID')
            if not tenant_id:
                return JsonResponse({'error': 'Authentication or Tenant Header required.'}, status=401)
            # ... resolve tenant from header like before
            
        return self.get_response(request)