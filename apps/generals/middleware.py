from django.http import JsonResponse

from config.settings import REST_FRAMEWORK


class APIVersionMiddleware:
    """
    Middleware for checking the project version using URL
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip("/").split("/")
        if len(path) > 1 and path[0] == "api":
            version = path[1]
            if version in REST_FRAMEWORK.get("ALLOWED_VERSIONS"):
                request.version = version
            else:
                return JsonResponse({"error": "Unsupported API version"}, status=400)
        else:
            request.version = None

        return self.get_response(request)
