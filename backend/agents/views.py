from rest_framework.views import APIView
from rest_framework.response import Response


class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print("Received webhook data:", data)
        print("Args:", args)
        print("Kwargs:", kwargs)
        return Response({"status": "success"}, status=200)
