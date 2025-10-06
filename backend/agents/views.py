from rest_framework.views import APIView
from rest_framework.response import Response


class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print("Received webhook data:", data)
            print("Args:", args)
            print("Kwargs:", kwargs)
            return Response({"status": "success"}, status=200)
        except Exception as e:
            print("Error processing webhook:", e)
            return Response({"status": "error", "message": str(e)}, status=400)
