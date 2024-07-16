from django.http import JsonResponse
from .models import AdminAPIKey


class AdminAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_endpoints = ['/api/add_train/'] 
        if any(request.path.startswith(endpoint) for endpoint in admin_endpoints):
            api_key = request.headers.get('API-Key')
            if not api_key or not AdminAPIKey.objects.filter(api_key=api_key).exists():
                return JsonResponse({'error': 'Unauthorized'}, status=401)
        response = self.get_response(request)
        return response
