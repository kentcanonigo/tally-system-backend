from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt #Since you're building a REST API, you can disable CSRF checks for API requests. This bypasses CSRF protection for this specific view.
def test_api(request):
    return JsonResponse({"request_method": request.method})