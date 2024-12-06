from rest_framework.views import APIView
from rest_framework.response import Response


class RegistrationV2View(APIView):
    def get(self, request):
        return Response("This is version2", status=200)
