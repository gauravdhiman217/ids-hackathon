from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import process_ticket_data


class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        ticket_id = data.get("TicketID")
        if ticket_id:
            process_ticket_data.delay(ticket_id)
        return Response({"status": "success"}, status=200)

        return Response({"status": "success"}, status=200)
